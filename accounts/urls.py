from django.urls import path
from .views import get_accounts, create_accounts, deposit, withdraw

urlpatterns = [
    path('',get_accounts),
    path('create/', create_accounts),
    path('deposit/', deposit),
    path('withdraw/', withdraw),
]
