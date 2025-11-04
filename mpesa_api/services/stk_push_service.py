import json
import requests
import logging
from decouple import config
from datetime import datetime
from ..utils import generate_access_token
from ..utils import generate_password
from ..models import MpesaTransaction

logger = logging.getLogger('mpesa')


def send_stk_push(request):
    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        body = {}
    phone = body.get('phone')
    amount = body.get('amount')
    account_reference = body.get('account_reference', 'DefaultRef')
    description = body.get('description', 'Payment Request')

    access_token = generate_access_token()
    password, timestamp = generate_password()

    payload = {
        "BusinessShortCode": config('MPESA_SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": config('MPESA_SHORTCODE'),
        "PhoneNumber": phone,
        "CallBackURL": config('MPESA_CALLBACK_URL'),
        "AccountReference": account_reference,
        "TransactionDesc": description
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{config('MPESA_BASE_URL')}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    # Debug
    # if response.status_code != 200:
    #     print("M-PESA error", response.text)

    response.raise_for_status()
    data = response.json()

    MpesaTransaction.objects.create(
        phone_number=phone,
        amount=amount,
        checkout_request_id=data.get("CheckoutRequestID"),
        merchant_request_id=data.get("MerchantRequestID"),
        status="Pending"
    )

    logger.info(f"STK Push initiated for {phone} - Amount: {amount}")
    return data
