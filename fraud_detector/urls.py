"""
URL configuration for fraud_detector project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# fraud_detector/urls.py
from django.contrib import admin
from django.urls import path, include
from fraud_app.views import home, check_transaction_web
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "OK", "message": "Fraud Detector API is running!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('check/', check_transaction_web, name='fraud-check-web'),
    path('api/', include('fraud_app.api.urls')),
    path('api/health/', health_check, name='health'),
]


 