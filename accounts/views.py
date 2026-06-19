from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, DepositSerializer, WithdrawSerializer

@api_view(['GET'])
def get_accounts(req):
    accounts=Account.objects.all()
    ser=AccountSerializer(accounts, many=True)
    return Response(ser.data)

@api_view(['POST'])
def create_accounts(req):
    ser=AccountSerializer(data=req.data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data)
    return Response(ser.errors)

@api_view(['POST'])
def deposit(request):
    serializer = DepositSerializer(data = request.data)
    
    if serializer.is_valid():
        account_number = serializer.validated_data['account_number']
        amount = serializer.validated_data['amount']
        
        account = Account.objects.get(account_number=account_number)
        account.balance+=amount
        account.save()
        
        transaction=Transaction.objects.create(
            account = account,
            transaction_type = 'Deposit',
            amount = amount,
            remarks = 'Deposit'
        )
        transaction.save()
        
        return Response(
            {
                'message':'Deposit Successful',
                'new_balance':account.balance
            }
        )
    return Response(serializer.errors)


@api_view(['POST'])
def withdraw(request):
    serializer = WithdrawSerializer(data = request.data)
    
    if serializer.is_valid():
        account_number = serializer.validated_data['account_number']
        amount = serializer.validated_data['amount']

        account = Account.objects.get(account_number=account_number)
        if account.balance >= amount:
            account.balance -= amount
            account.save()
            
            Transaction.objects.create(
                account = account,
                transaction_type = 'Withdrawal',
                amount = amount,
                remarks = 'Withdraw'
            )
        
            return Response({
                "message": "Withdrawal successful!",
                "new_balance" : account.balance
            })
            
        else:
            return Response(
                {"error":"Insufficient Balance"}
            )
    return Response(serializer.errors)
    