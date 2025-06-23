from src.config import settings
import yookassa
from yookassa import Payment
import uuid


yookassa.Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
yookassa.Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create(amount, chat_id, description):
    id_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{settings.BOT_USERNAME}"
        },
        "capture": True,
        "metadata": {
            "chat_id": chat_id
        },
        "description": {
            description
        }
    }, id_key)

    return payment.confirmation.confirmation_url, payment.id