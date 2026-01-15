import uuid
from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    transaction_id = models.CharField(
        max_length=20, 
        unique=True, 
        default=lambda: str(uuid.uuid4())[:8].upper()
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    card_number = models.CharField(max_length=19)
    card_last4 = models.CharField(max_length=4)
    merchant = models.CharField(max_length=100, default="Inconnu")
    fraud_score = models.FloatField(default=0.0)
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_id} - {self.amount} FCFA ({'FRAUDE' if self.is_flagged else 'OK'})"

class Alert(models.Model):
    ALERT_TYPES = [
        ('FRAUD', 'Fraude détectée'),
        ('HIGH_AMOUNT', 'Montant élevé'),
        ('SUSPICIOUS', 'Comportement suspect'),
    ]
    
    SEVERITY = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyen'),
        ('HIGH', 'Élevé'),
        ('CRITICAL', 'Critique'),
    ]
    
    transaction_id = models.CharField(max_length=20)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY, default='LOW')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.alert_type} - {self.transaction_id}"