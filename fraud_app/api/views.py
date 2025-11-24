from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Transaction
from ..ml.predictor import FraudDetector
from ..tasks import send_fraud_alert

class FraudCheckView(APIView):
    def post(self, request):
        data = request.data

        required_fields = ['transaction_id', 'amount', 'card_last4', 'merchant']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return Response({"error": f"Champs manquants : {missing}"}, status=status.HTTP_400_BAD_REQUEST)

        # Créer la transaction
        tx = Transaction.objects.create(
            transaction_id=data['transaction_id'],
            amount=data['amount'],
            card_last4=data['card_last4'],
            merchant=data['merchant']
        )

        # Prédiction
        try:
            result = FraudDetector.predict(data)
            tx.fraud_score = result['fraud_score']
            tx.is_flagged = result['is_flagged']
            tx.save()

            # Alerte asynchrone si fraude
            if result['is_flagged']:
                send_fraud_alert.delay(tx.id)

            return Response({
                "transaction_id": tx.transaction_id,
                "fraud_score": result['fraud_score'],
                "is_flagged": result['is_flagged'],
                "status": "FRAUDE" if result['is_flagged'] else "OK"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)