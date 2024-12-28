from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
import requests
import hashlib
import base64
import json

from Ecomm.models import Category,Sub_category
from orders.models import Order,OrderProduct
from .models import Payment

from django.views.decorators.csrf import csrf_exempt

def initiate_payment(request, order_ids):
    categories = Category.objects.all()  # Fetch all categories
    subcategories = Sub_category.objects.all()
    orders = Order.objects.filter(id__in=order_ids, buyer=request.user, status="Pending")

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    # Check if the order exists
    try:
        order = Order.objects.get(id=order_ids, buyer=request.user, status="Pending")
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found or already processed"}, status=400)

    payments = []
    for order in orders:
        try:
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={"amount": order.total_price, "user": request.user},
            )
            if not created:
                return JsonResponse({"error": f"Payment already exists for order {order.id}"}, status=400)
            payments.append(payment)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
    
    # Handle PhonePe payment initiation
    for payment in payments:
        payload = {
            "merchantId": settings.PHONEPE_MERCHANT_ID,
            "transactionId": f"ORDER-{payment.id}",
            "amount": int(payment.amount * 100),  # Convert to paisa
            "merchantUserId": str(request.user.id),
            "redirectUrl": settings.PHONEPE_CALLBACK_URL,  # Callback after payment
        }
        headers = {
            "Content-Type": "application/json",
            "X-VERIFY": generate_signature(payload),
        }

        response = requests.post(settings.PHONEPE_BASE_URL + "/payment/initiate", json=payload, headers=headers)
        
        # Check the response from PhonePe
        if response.status_code == 200:
            data = response.json()
            redirect_url = data['data']['redirectUrl']  # URL to redirect user for payment
            payment.phonepe_transaction_id = data['data']['transactionId']
            payment.save()
            return redirect(redirect_url)  # Redirect user to PhonePe payment page
        else:
            return JsonResponse({"error": "Payment initiation failed", "details": response.json()}, status=400)

    return JsonResponse({"error": "Failed to process payment"}, status=400)


def generate_signature(payload):
    """Generate HMAC signature for PhonePe requests."""
    key = settings.PHONEPE_API_KEY
    payload_str = f"{payload}|/payment/initiate|{key}"
    hashed = hashlib.sha256(payload_str.encode("utf-8")).digest()
    return base64.b64encode(hashed).decode("utf-8")



@csrf_exempt
def phonepe_callback(request):
    """Handles PhonePe payment status updates."""
    data = request.body.decode("utf-8")
    received_signature = request.headers.get("X-VERIFY")
    if received_signature != generate_signature(data):
        return JsonResponse({"error": "Invalid signature"}, status=400)

    payment_response = json.loads(data)
    payment = Payment.objects.get(phonepe_transaction_id=payment_response['transactionId'])
    payment.status = payment_response['status']
    payment.save()
    return JsonResponse({"message": "Callback received"})
    #if payment_response['status'] == "SUCCESS":
     #   return render(request, 'payments/payment_success.html', {'payment': payment})
    #else:
     #   return render(request, 'payments/payment_failure.html', {'payment': payment})
