from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, DepositSerializer, WithdrawSerializer, TransferSerializer
from django.db import transaction

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
    

@api_view(['POST'])
def transfer(request):
    serializer = TransferSerializer(data = request.data)
    
    if serializer.is_valid():
        with transaction.atomic():
            sender_account = serializer.validated_data['sender_account']
            receiver_account = serializer.validated_data['receiver_account']
            amount = serializer.validated_data['amount']

            try:
                sender=Account.objects.get(account_number = sender_account)
            except Account.DoesNotExist:
                return Response({
                    'error':"Sender account not found!"
                })
            
            try:
                receiver= Account.objects.get(account_number = receiver_account)
            except Account.DoesNotExist:
                return Response({
                    'error':"Receiver's account not found"
                })
                
            if sender.account_number == receiver.account_number:
                return Response ({
                    'message': 'Self Transfer not applicable!'
                })
            if sender.balance>=amount:
                receiver.balance+=amount
                sender.balance -=amount
                sender.save()
                receiver.save()
                
                Transaction.objects.create(
                    account = sender,
                    transaction_type =  'Transfer_out',
                    amount = amount,
                    remarks = f'transferred to {receiver.account_number}'
                )
                
                Transaction.objects.create(
                    account = receiver,
                    transaction_type = 'Transfer_in',
                    amount = amount,
                    remarks = f'transferred from {sender.account_number}'
                )
                
                return Response({'message':'Transfer Successful!',
                                'balance':sender.balance})
            else:
                return Response({'message':'Insufficient Balance!!'})
    else:
        return Response(serializer.errors)