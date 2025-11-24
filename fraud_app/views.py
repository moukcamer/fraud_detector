# fraud_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Transaction
from .ml.predictor import FraudDetector
from .tasks import send_fraud_alert
import random

def home(request):
    if not request.session.session_key:
        request.session.create()
    request.session['counter'] = request.session.get('counter', 0) + 1
    return render(request, 'fraud/home.html')

def check_transaction_web(request):
    if request.method == "POST":
        data = request.POST.copy()
        # Construire le dictionnaire complet pour le modèle
        tx_data = {
            'transaction_id': data['transaction_id'],
            'amount': float(data['amount']),
            'card_last4': data['card_last4'],
            'merchant': data['merchant'],
        }
        # Ajouter les features V1-V28
        for i in range(1, 29):
            tx_data[f'V{i}'] = float(data.get(f'V{i}', random.uniform(-2.5, 2.5)))

        # Prédiction
        result = FraudDetector.predict(tx_data)
        
        # Sauvegarde
        tx = Transaction.objects.create(
            transaction_id=tx_data['transaction_id'],
            amount=tx_data['amount'],
            card_last4=tx_data['card_last4'],
            merchant=tx_data['merchant'],
            fraud_score=result['fraud_score'],
            is_flagged=result['is_flagged']
        )
        if result['is_flagged']:
            send_fraud_alert.delay(tx.id)
            messages.error(request, f"FRAUDE détectée ! Score = {result['fraud_score']:.5f}")
        else:
            messages.success(request, f"Transaction légitime (score = {result['fraud_score']:.5f})")

        return render(request, 'fraud/result.html', {
            'is_flagged': result['is_flagged'],
            'fraud_score': result['fraud_score']
        })
    
    return redirect('home')