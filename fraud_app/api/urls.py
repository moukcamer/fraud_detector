from django.urls import path
from .views import FraudCheckView

urlpatterns = [
    path('check/', FraudCheckView.as_view(), name='fraud-check'),
]