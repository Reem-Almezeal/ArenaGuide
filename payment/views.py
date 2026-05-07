from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
from django.contrib import messages
from booking.models import Booking, Ticket
from .models import PaymentTransaction
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def checkout(request, booking_id:HttpRequest):
    booking = get_object_or_404(
        Booking.objects.select_related("user", "match"),
        id=booking_id,
        user=request.user,
    )

    payment, created = PaymentTransaction.objects.get_or_create(
        booking=booking,
        defaults={
            "user": booking.user,
            "amount": booking.total_price,
            "status": PaymentTransaction.Status.PENDING,
            "provider": PaymentTransaction.Provider.MOYASAR,
        }
    )
    callback_url = request.build_absolute_uri(
    reverse("payment:payment_success", args=[booking.id])
    )

    return render(request, "payment/payment_check.html", {
        "booking": booking,
        "payment": payment,
        "moyasar_publishable_key": settings.MOYASAR_PUBLISHABLE_KEY,
        "callback_url": callback_url,
    })

@login_required
def payment_success(request, booking_id:HttpRequest):
    moyasar_id = request.GET.get("id")
    status = request.GET.get("status")
    message = request.GET.get("message")

    booking = get_object_or_404(
        Booking.objects.select_related("user", "match"),
        id=booking_id,
        user=request.user,
    )

    payment = get_object_or_404(PaymentTransaction, booking=booking)

    if status != "paid":
        payment.status = PaymentTransaction.Status.FAILED
        payment.failure_reason = message or "Payment failed"
        payment.save()
        messages.error(request, "Payment was not completed.")
        return redirect("payment:checkout", booking_id=booking.id)

    payment.status = PaymentTransaction.Status.SUCCESS
    payment.provider_reference = moyasar_id
    payment.paid_at = timezone.now()
    payment.save()

    booking.status = Booking.Status.CONFIRMED
    booking.save()

    messages.success(request, "Payment successful. Your ticket has been confirmed.")

    return render(request, "payment/payment_success.html", {
        "booking": booking,
        "payment": payment,
    })