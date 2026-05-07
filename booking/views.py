import hashlib
import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpRequest
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from match.models import Match
from payment.models import PaymentTransaction
from stadium.models import Parking
from .models import Booking, IdentityVerification, Seat, Ticket, TicketHolder,ParkingReservation
from django.shortcuts import render
from decimal import Decimal
from django.db.models import Q
from payment.views import checkout


def make_identity_hash(id_type, id_number:HttpRequest):
    raw = f"{id_type}:{id_number}:{settings.SECRET_KEY}"
    return hashlib.sha256(raw.encode()).hexdigest()


def verify_last4_match(id_number, id_last4:HttpRequest):
    return True


def validate_id_number(id_type, id_number:HttpRequest):
    errors = []

    if id_type in ["national_id", "iqama"]:
        if not re.match(r"^\d{10}$", id_number):
            errors.append("National ID / Iqama must be exactly 10 digits.")

    elif id_type == "passport":
        if not re.match(r"^[A-Za-z0-9]{6,12}$", id_number):
            errors.append("Passport number must be 6 to 12 letters or numbers.")

    else:
        errors.append("Invalid ID type.")
    return errors

# Placeholder for future third-party identity verification API integration
def verify_identity_with_provider(data:HttpRequest):
    return True


def validate_visitor_data(full_name, email, phone, id_last4, date_of_birth, id_document=None):
    errors = []

    if not full_name or len(full_name.strip()) < 5:
        errors.append("Full name must be at least 5 characters.")

    if len(full_name.split()) < 2:
        errors.append("Please enter your full name.")

    if not date_of_birth:
        errors.append("Date of birth is required.")

    try:
        validate_email(email)
    except ValidationError:
        errors.append("Please enter a valid email address.")

    if not re.match(r"^05\d{8}$", phone):
        errors.append("Phone number must be a valid Saudi number starting with 05.")

    if not re.match(r"^\d{4}$", id_last4):
        errors.append("ID / Passport last 4 digits must contain exactly 4 numbers.")

    if id_document:
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        max_size = 5 * 1024 * 1024

        if id_document.content_type not in allowed_types:
            errors.append("ID document must be JPG or PNG.")

        if id_document.size > max_size:
            errors.append("ID document size must be less than 5MB.")
    return errors


def book_ticket_page(request, match_id:HttpRequest):
    match = get_object_or_404(
        Match.objects.select_related("home_team", "away_team", "stadium"),
        id=match_id,
    )

    booked_seat_ids = Ticket.objects.filter(
        match=match,
        status__in=[Ticket.Status.ACTIVE, Ticket.Status.USED],
    ).values_list("seat_id", flat=True)

    seats = Seat.objects.filter(
        stadium=match.stadium,
        is_active=True,
    ).select_related("category", "gate").order_by(
        "category__base_price", "section", "row", "number"
    )

    categories = {}

    for seat in seats:
        category_name = seat.category.name

        if category_name not in categories:
            categories[category_name] = {
                "category": seat.category,
                "seats": [],
            }

        categories[category_name]["seats"].append({
            "id": seat.id,
            "code": seat.code,
            "section": seat.section,
            "row": seat.row,
            "number": seat.number,
            "price": seat.category.base_price,
            "gate": seat.gate.name if seat.gate else "N/A",
            "view_quality": seat.get_view_quality_display(),
            "is_shaded": seat.is_shaded,
            "sun_exposure": seat.get_sun_exposure_display(),
            "notes": seat.notes,
            "is_booked": seat.id in booked_seat_ids,
        })

    parking_options = Parking.objects.filter(
        stadium=match.stadium,
        status=Parking.Status.AVAILABLE,
    )

    return render(request, "booking/booking_ticket.html", {
        "match": match,
        "categories": categories,
        "parking_options": parking_options,
    })


@login_required
@transaction.atomic
def booking_details(request, match_id:HttpRequest):
    match = get_object_or_404(
        Match.objects.select_for_update().select_related(
            "home_team", "away_team", "stadium"
        ),
        id=match_id,
    )

    seat_ids_value = (
        request.POST.get("seat_ids")
        or request.session.get(f"booking_seats_{match.id}")
    )

    parking_id = (
        request.POST.get("parking_id")
        or request.session.get(f"booking_parking_{match.id}")
    )

    if not seat_ids_value:
        messages.error(request, "Please select at least one seat.")
        return redirect("booking:book_ticket_page", match_id=match.id)

    seat_ids = [seat_id for seat_id in seat_ids_value.split(",") if seat_id]

    seats = list(
        Seat.objects.select_related("category", "gate", "stadium").filter(
            id__in=seat_ids,
            stadium=match.stadium,
            is_active=True,
        )
    )

    if len(seats) != len(seat_ids):
        messages.error(request, "Some selected seats are invalid.")
        return redirect("booking:book_ticket_page", match_id=match.id)

    parking = None
    if parking_id:
        parking = get_object_or_404(
            Parking.objects.select_for_update(),
            id=parking_id,
            stadium=match.stadium,
        )

    request.session[f"booking_seats_{match.id}"] = ",".join(seat_ids)

    if parking:
        request.session[f"booking_parking_{match.id}"] = parking.id
    else:
        request.session.pop(f"booking_parking_{match.id}", None)

    if Ticket.objects.filter(
        match=match,
        seat__in=seats,
        status__in=[Ticket.Status.ACTIVE, Ticket.Status.USED],
    ).exists():
        messages.error(request, "One or more selected seats are already booked.")
        return redirect("booking:book_ticket_page", match_id=match.id)

    if not match.is_booking_open:
        messages.error(request, "Booking is currently closed for this match.")
        return redirect("match:match_detail", match_id=match.id)

    if match.available_tickets < len(seats):
        messages.error(request, "Not enough tickets are available for this match.")
        return redirect("match:match_detail", match_id=match.id)

    if parking and hasattr(parking, "is_available"):
        parking_available = parking.is_available
        if callable(parking_available):
            parking_available = parking_available()

        if not parking_available:
            messages.error(request, "Selected parking area is no longer available.")
            return redirect("booking:book_ticket_page", match_id=match.id)

    total_price = sum(seat.category.base_price for seat in seats)

    if request.method == "POST" and request.POST.get("booking_details_submit") == "1":
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()

        ticket_holders = []
        used_hashes = set()

        for index, seat in enumerate(seats, start=1):
            full_name = request.POST.get(f"full_name_{index}", "").strip()
            holder_type = request.POST.get(f"holder_type_{index}", "").strip()
            date_of_birth = request.POST.get(f"date_of_birth_{index}", "").strip()
            id_type = request.POST.get(f"id_type_{index}", "").strip()
            id_number = request.POST.get(f"id_number_{index}", "").strip()
            id_last4 = request.POST.get(f"id_last4_{index}", "").strip()
            id_document = request.FILES.get(f"id_document_{index}")

            errors = validate_visitor_data(
                full_name=full_name,
                email=email,
                phone=phone,
                id_last4=id_last4,
                date_of_birth=date_of_birth,
                id_document=id_document,
            )
            errors += validate_id_number(id_type, id_number)
            if not re.match(r"^\d{4}$", id_last4):
                errors.append("Last 4 digits must contain exactly 4 numbers.")

            if not verify_last4_match(id_number, id_last4):
                errors.append("Last 4 digits do not match the ID number.")

            id_hash = make_identity_hash(id_type, id_number)

            if errors:
                for error in errors:
                    messages.error(request, f"Ticket {index}: {error}")

                return render(request, "booking/booking_details.html", {
                    "match": match,
                    "seats": seats,
                    "parking": parking,
                    "total_price": total_price,
                })
            if id_hash in used_hashes:
                messages.error(request, f"Ticket {index}: The same identity cannot be used twice.")
                return render(request, "booking/booking_details.html", {
                    "match": match,
                    "seats": seats,
                    "parking": parking,
                    "total_price": total_price,
                })

            used_hashes.add(id_hash)

            if Ticket.objects.filter( match=match,holder__id_hash=id_hash,status__in=[Ticket.Status.ACTIVE, Ticket.Status.USED],).exists():
                messages.error(request, "This ID already has a ticket for this match.")
                return render(request, "booking/booking_details.html", {
                        "match": match,
                        "seats": seats,
                        "parking": parking,
                        "total_price": total_price,
                    })

        ticket_holders.append({
            "seat": seat,
            "full_name": full_name,
            "holder_type": holder_type,
            "date_of_birth": date_of_birth,
            "id_type": id_type,
            "id_number": id_number,
            "id_last4": id_last4,
            "id_document": id_document,
            "id_hash": id_hash,
        })

        first_holder = ticket_holders[0]

        identity_data = {
            "full_name": first_holder["full_name"],
            "email": email,
            "phone": phone,
            "id_last4": first_holder["id_last4"],
            "id_hash": first_holder["id_hash"],
        }

        if not verify_identity_with_provider(identity_data):
            messages.error(request, "Identity verification failed. Please review your information.")
            return render(request, "booking/booking_details.html", {
                "match": match,
                "seats": seats,
                "parking": parking,
                "total_price": total_price,
            })

        IdentityVerification.objects.update_or_create(
            user=request.user,
            defaults={
                "provider": IdentityVerification.Provider.MOCK,
                "status": IdentityVerification.Status.VERIFIED,
                "id_last4": first_holder["id_last4"],
                "id_hash": first_holder["id_hash"],
                "verified_full_name": first_holder["full_name"],
                "id_document": first_holder["id_document"],
                "verified_at": timezone.now(),
            },
        )

        Booking.objects.filter(
            user=request.user,
            match=match,
            status=Booking.Status.PENDING_PAYMENT,
        ).update(status=Booking.Status.CANCELLED)

        booking = Booking.objects.create(
            user=request.user,
            match=match,
            total_price=total_price,
            status=Booking.Status.PENDING_PAYMENT,
            identity_checked=True,
        )

        for holder_data in ticket_holders:
            holder, _ = TicketHolder.objects.get_or_create(
                id_hash=holder_data["id_hash"],
                defaults={
                    "full_name": holder_data["full_name"],
                    "holder_type": holder_data["holder_type"],
                    "date_of_birth": holder_data["date_of_birth"],
                    "id_last4": holder_data["id_last4"],
                    "id_document": holder_data["id_document"],
                },
            )

            Ticket.objects.create(
                booking=booking,
                user=request.user,
                match=match,
                seat=holder_data["seat"],
                gate=holder_data["seat"].gate,
                holder=holder,
                price=holder_data["seat"].category.base_price,
                status=Ticket.Status.ACTIVE,
            )

        PaymentTransaction.objects.create(
            booking=booking,
            user=request.user,
            amount=booking.total_price,
            status=PaymentTransaction.Status.PENDING,
            provider=PaymentTransaction.Provider.MOYASAR,
        )

        if parking:
            request.session[f"booking_parking_{booking.id}"] = parking.id
        return redirect("payment:checkout", booking_id=booking.id)

    return render(request, "booking/booking_details.html", {
        "match": match,
        "seats": seats,
        "parking": parking,
        "total_price": total_price,
    })


@login_required
def my_tickets(request:HttpRequest):
    today = timezone.localdate()

    tickets = Ticket.objects.filter(user=request.user).select_related("booking","match","match__home_team","match__away_team","match__stadium","seat","gate", "parking_reservation",)
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    date_filter = request.GET.get("date", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    if search:
        tickets = tickets.filter(
            Q(ticket_code__icontains=search) |
            Q(match__home_team__name__icontains=search) |
            Q(match__away_team__name__icontains=search) |
            Q(match__stadium__name__icontains=search)
        )

    if status:
        tickets = tickets.filter(status=status)

    if date_filter == "today":
        tickets = tickets.filter(match__start_datetime__date=today)
    elif date_filter == "upcoming":
        tickets = tickets.filter(match__start_datetime__date__gt=today)
    elif date_filter == "past":
        tickets = tickets.filter(match__start_datetime__date__lt=today)

    if sort == "oldest":
        tickets = tickets.order_by("issued_at")
    elif sort == "match_date":
        tickets = tickets.order_by("match__start_datetime")
    else:
        tickets = tickets.order_by("-issued_at")

    return render(request, "booking/my_tickets.html", {
        "tickets": tickets,
        "search": search,
        "status": status,
        "date_filter": date_filter,
        "sort": sort,
        "today": today,
    })


@login_required
def seat_map_page(request, ticket_id:HttpRequest):
    ticket = get_object_or_404(Ticket.objects.select_related("match","match__home_team","match__away_team","match__stadium","seat","gate",),
        id=ticket_id,
        user=request.user,
        status=Ticket.Status.ACTIVE,
    )

    return render(request, "booking/seat_map.html", {
        "ticket": ticket,
    })


@login_required
def reserve_parking(request, ticket_id:HttpRequest):
    ticket = get_object_or_404(Ticket.objects.select_related("booking","match","match__home_team","match__away_team","match__stadium","seat","seat__gate","gate",),
        id=ticket_id,
        user=request.user,
        status=Ticket.Status.ACTIVE,
    )

    gate = ticket.gate or ticket.seat.gate

    if request.method == "POST":
        parking_type = request.POST.get("parking_type")

        if not parking_type:
            messages.error(request, "Please select a parking type.")
            return redirect("booking:reserve_parking", ticket_id=ticket.id)

        price = 75 if parking_type == "vip" else 40

        reservation, created = ParkingReservation.objects.get_or_create(
            ticket=ticket,
            defaults={
                "user": request.user,
                "match": ticket.match,
                "stadium": ticket.match.stadium,
                "reservation_time": timezone.now(),
                "price": price,
                "paid": False,
                "status": ParkingReservation.Status.PENDING,
            }
        )

        reservation.price = price
        reservation.paid = False
        reservation.status = ParkingReservation.Status.PENDING
        reservation.save()

        return checkout(request, reservation.id)

    return render(request, "booking/reserve_parking.html", {
        "ticket": ticket,
        "gate": gate,
    })


@login_required
def parking_checkout(request, reservation_id:HttpRequest):
    reservation = get_object_or_404(
        ParkingReservation.objects.select_related("user","ticket","match","stadium",),
        id=reservation_id,
        user=request.user,
        status=ParkingReservation.Status.PENDING,
    )

    if reservation.paid:
        messages.info(request, "Parking payment already completed.")
        return redirect("booking:my_tickets")

    return render(request, "payment/parking_checkout.html", {
        "reservation": reservation,
        "moyasar_publishable_key": settings.MOYASAR_PUBLISHABLE_KEY,
    })


@login_required
def parking_success(request, reservation_id:HttpRequest):
    reservation = get_object_or_404(
        ParkingReservation.objects.select_related("user","ticket", "match", "stadium",),
        id=reservation_id,
        user=request.user,
    )

    status = request.GET.get("status")

    if status != "paid":
        messages.error(request, "Parking payment was not completed.")
        return checkout(request, reservation.id)

    reservation.paid = True
    reservation.status = ParkingReservation.Status.ACTIVE
    reservation.save(update_fields=["paid", "status"])

    messages.success(request, "Parking payment successful.")
    return redirect("booking:my_tickets")