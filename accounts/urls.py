from django.urls import path
from .views import get_accounts, create_accounts, deposit, withdraw, transfer

urlpatterns = [
    path('',get_accounts),
    path('create/', create_accounts),
    path('deposit/', deposit),
    path('withdraw/', withdraw),
    path('transfer/', transfer),
]
