from django.contrib import admin
from .models import Transaction, Alert

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'amount', 'card_last4', 'fraud_score', 'is_flagged', 'created_at']
    list_filter = ['is_flagged', 'created_at', 'fraud_score']
    search_fields = ['transaction_id', 'card_last4', 'merchant']
    readonly_fields = ['created_at']
    list_per_page = 50
    ordering = ['-created_at']
    
    fieldsets = (
        ('Transaction', {
            'fields': ('transaction_id', 'amount', 'card_number', 'card_last4', 'merchant')
        }),
        ('Analyse IA', {
            'fields': ('fraud_score', 'is_flagged'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'alert_type', 'severity', 'created_at']
    list_filter = ['alert_type', 'severity', 'created_at']
    search_fields = ['transaction_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']