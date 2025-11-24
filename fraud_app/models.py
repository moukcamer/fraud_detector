from django.db import models

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    card_last4 = models.CharField(max_length=4)
    merchant = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    fraud_score = models.FloatField(null=True, blank=True)
    is_flagged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['is_flagged']),
        ]

    def __str__(self):
        return f"{self.transaction_id} | {self.amount}€ | {'FRAUDE' if self.is_flagged else 'OK'}"