from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields='__all__'
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'
        
    
class DepositSerializer(serializers.Serializer):
    account_number= serializers.CharField(max_length=12)
    
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    
    
class WithdrawSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=12)
    
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    

class TransferSerializer(serializers.Serializer):
    sender_account = serializers.CharField(max_length= 12)
    receiver_account = serializers.CharField(max_length= 12)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    