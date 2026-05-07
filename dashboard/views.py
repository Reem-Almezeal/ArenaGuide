from django.shortcuts import render,redirect,get_object_or_404
from .models import GateStatusUpdate
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.decorators import login_required 
from django.db.models import Count
from .models import GateStatusUpdate
from match.models import Match
from stadium.models import Gate
from booking.models import Ticket
from booking.models import Ticket, TicketHolder
from booking.views import make_identity_hash
from django.contrib.auth import  logout
from django.contrib import messages
from stadium.models import Gate


def organizer_dashboard(request:HttpRequest):
    return render(
        request,
        "dashboard/organizer_dashboard.html"
    )



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


from stadium.models import Gate

@login_required(login_url="account:login")
def gate_management_view(request):
    gates = Gate.objects.select_related("stadium").all()

    return render(
        request,
        "dashboard/gate_management.html",
        {
            "gates": gates
        }
    )


@login_required(login_url="account:login")
def update_gate_status(request, gate_id):
    if not request.user.is_organizer():
        return redirect("core:home")
    gate = get_object_or_404(Gate, id=gate_id)
    status = request.POST.get("status")

    if status in [
        Gate.Status.OPEN,
        Gate.Status.CLOSED,
        Gate.Status.MAINTENANCE
    ]:
        gate.status = status
        gate.save()

    return redirect("dashboard:gate_management")