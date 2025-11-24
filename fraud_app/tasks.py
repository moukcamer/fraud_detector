from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Transaction

@shared_task
def send_fraud_alert(transaction_id):
    try:
        tx = Transaction.objects.get(id=transaction_id)
        subject = f"[ALERTE FRAUDE] Transaction {tx.transaction_id}"
        message = f"""
        FRAUDE DÉTECTÉE !
        ID : {tx.transaction_id}
        Montant : {tx.amount} €
        Carte : **** {tx.card_last4}
        Commerçant : {tx.merchant}
        Score de fraude : {tx.fraud_score:.5f}
        Date : {tx.timestamp}
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['security@bank.com'],  # Change avec ton email
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erreur envoi alerte : {e}")