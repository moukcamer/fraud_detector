# fraud_app/urls.py

from django.urls import path
from .api.views import FraudCheckView
from .views import home, check_transaction_web  # ← vues avec templates

app_name = 'fraud_app'

urlpatterns = [
    # ==== Interface web (templates) ====
    path('', home, name='home'),                              # Page d'accueil avec formulaire
    path('check/', check_transaction_web, name='fraud-check-web'),  # Traitement du formulaire

    # ==== API REST (JSON) ====
    path('api/check/', FraudCheckView.as_view(), name='fraud-check-api'),
    
    # Optionnel : santé de l’API
    path('api/health/', lambda request: JsonResponse({"status": "OK", "app": "fraud_app"}), name='api-health'),
]