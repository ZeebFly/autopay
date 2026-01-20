import requests
import uuid
from config import *
from database import create_order

def create_qris(user_id):
    invoice = str(uuid.uuid4())

    payload = {
        "method": "QRIS",
        "merchant_ref": invoice,
        "amount": PRICE,
        "customer_name": str(user_id)
    }

    headers = {
        "Authorization": f"Bearer {TRIPAY_API_KEY}"
    }

    res = requests.post(
        "https://tripay.co.id/api/transaction/create",
        json=payload,
        headers=headers
    ).json()

    create_order(user_id, invoice, PRICE)

    return res["data"]["qr_url"]
