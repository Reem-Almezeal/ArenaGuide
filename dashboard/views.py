from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import GateStatusUpdate
from match.models import Match
from stadium.models import Gate
from booking.models import Ticket, TicketHolder
from booking.views import make_identity_hash
from django.db.models import Avg



@login_required
def organizer_dashboard(request:HttpRequest):
    latest_updates = GateStatusUpdate.objects.select_related("gate","alternative_gate","match","match__home_team","match__away_team","updated_by",).order_by("-created_at")[:6]
    open_count = GateStatusUpdate.objects.filter(status=GateStatusUpdate.Status.OPEN).count()
    crowded_count = GateStatusUpdate.objects.filter(status=GateStatusUpdate.Status.CROWDED).count()
    emergency_count = GateStatusUpdate.objects.filter(status=GateStatusUpdate.Status.EMERGENCY).count()
    closed_count = GateStatusUpdate.objects.filter(status=GateStatusUpdate.Status.CLOSED).count()
    total_tickets = Ticket.objects.count()
    active_tickets = Ticket.objects.filter(status=Ticket.Status.ACTIVE).count()
    current_match = Match.objects.select_related("home_team","away_team","stadium",).order_by("-start_datetime").first()

    total_gates = Gate.objects.count()

    context = {
        "latest_updates": latest_updates,
        "open_count": open_count,
        "crowded_count": crowded_count,
        "emergency_count": emergency_count,
        "closed_count": closed_count,
        "total_tickets": total_tickets,
        "active_tickets": active_tickets,
        "current_match": current_match,
        "total_gates": total_gates,
    }

    return render(request, "dashboard/organizer_dashboard.html", context)



@login_required
def verify_visitor(request:HttpRequest):
    ticket = None
    holder = None
    identity_number = ""
    id_type = ""
    error_message = ""

    if request.method == "POST":
        id_type = request.POST.get("id_type", "").strip()
        identity_number = request.POST.get("identity_number", "").strip()

        if not id_type or not identity_number:
            error_message = "Please enter identity type and identity number."
        else:
            id_hash = make_identity_hash(id_type, identity_number)
            holder = TicketHolder.objects.filter(
                id_hash=id_hash
            ).first()

            if holder:
                ticket = Ticket.objects.filter(
                    holder=holder
                ).select_related("user","holder","booking","seat","gate","match","match__home_team","match__away_team","match__stadium"
                ).order_by("-issued_at").first()

                if not ticket:
                    error_message = "No ticket found for this visitor."
            else:
                error_message = "No visitor found with this identity number."

    return render(request, "dashboard/verify_visitor.html", {"ticket": ticket,"holder": holder,"id_type": id_type,"identity_number": identity_number,"error_message": error_message, })



@login_required(login_url="account:login")
def gate_management_view(request):
    gates = Gate.objects.select_related("stadium").all()
    open_gates_count = gates.filter(status=Gate.Status.OPEN).count()
    closed_gates_count = gates.filter(status=Gate.Status.CLOSED).count()
    maintenance_gates_count = gates.filter( status=Gate.Status.MAINTENANCE).count()
    average_crowd = gates.aggregate(avg=Avg("crowd_percentage"))["avg"] or 0
    average_crowd = round(average_crowd)

    return render(
        request,
        "dashboard/gate_management.html",
        {
            "gates": gates,
            "open_gates_count": open_gates_count,
            "closed_gates_count": closed_gates_count,
            "maintenance_gates_count": maintenance_gates_count,
            "average_crowd": average_crowd,
        }
    )
@login_required(login_url="account:login")
def update_gate_status(request, gate_id):
    if not request.user.is_organizer():
        return redirect("core:home")

    gate = get_object_or_404(Gate, id=gate_id)

    if request.method != "POST":
        return redirect("dashboard:gate_management_view")

    current_match = Match.objects.select_related(
        "home_team", "away_team", "stadium"
    ).order_by("-start_datetime").first()

    if not current_match:
        messages.error(request, "No match found.")
        return redirect("dashboard:gate_management_view")

    status = request.POST.get("status")
    priority = request.POST.get("priority", GateStatusUpdate.Priority.NORMAL)
    alternative_gate_id = request.POST.get("alternative_gate")
    message = request.POST.get("message", "").strip()
    internal_note = request.POST.get("internal_note", "").strip()
    notify_users = request.POST.get("notify_users") == "on"

    crowd_percentage = request.POST.get("crowd_percentage", 0)
    try:
        crowd_percentage = int(crowd_percentage)
    except ValueError:
        crowd_percentage = 0

    crowd_percentage = max(0, min(crowd_percentage, 100))

    alternative_gate = None
    if alternative_gate_id:
        alternative_gate = get_object_or_404(Gate, id=alternative_gate_id)

    affected_tickets = Ticket.objects.filter(
        gate=gate,
        match=current_match,
        status=Ticket.Status.ACTIVE
    ).select_related("user", "match", "gate")

    affected_count = affected_tickets.count()

    update = GateStatusUpdate.objects.create(
        gate=gate,
        match=current_match,
        status=status,
        priority=priority,
        alternative_gate=alternative_gate,
        title=f"Gate {gate.name} Update",
        message=message,
        internal_note=internal_note,
        notify_users=notify_users,
        affected_ticket_count=affected_count,
        updated_by=request.user,
    )

    gate.status = status
    gate.crowd_percentage = crowd_percentage
    gate.save(update_fields=["status", "crowd_percentage"])

    if notify_users and message:
        try:
            from notification.models import Notification

            for ticket in affected_tickets:
                Notification.objects.create(
                    user=ticket.user,
                    title=update.title,
                    message=message,
                )

                if alternative_gate:
                    ticket.gate = alternative_gate
                    ticket.save(update_fields=["gate"])

            update.notification_sent = True
            update.save(update_fields=["notification_sent"])

            messages.success(
                request,
                f"Gate updated. {affected_count} visitors were notified."
            )

        except Exception:
            messages.warning(
                request,
                "Gate updated, but notifications could not be sent. Check Notification model fields."
            )
    else:
        messages.success(request, "Gate updated successfully.")

    return redirect("dashboard:gate_management_view")