from django.urls import path
from .views import get_accounts, create_accounts, deposit, withdraw, transfer, transaction_history

urlpatterns = [
    path('',get_accounts),
    path('create/', create_accounts),
    path('deposit/', deposit),
    path('withdraw/', withdraw),
    path('transfer/', transfer),
    path('accounts/<str:account_number>/transactions/', transaction_history)
]
