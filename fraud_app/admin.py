from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'amount', 'card_last4', 'merchant', 'fraud_score', 'is_flagged', 'timestamp')
    list_filter = ('is_flagged', 'timestamp')
    search_fields = ('transaction_id', 'card_last4', 'merchant')
    readonly_fields = ('transaction_id', 'timestamp', 'fraud_score', 'is_flagged')
    list_per_page = 50

    def has_add_permission(self, request):
        return False  # On crée uniquement via API