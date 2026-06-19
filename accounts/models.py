from django.db import models
from django.contrib.auth.models import User
import uuid

class Account(models.Model):
    account_number = models.CharField(max_length=12, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default = 0)

    ACCOUNT_TYPES= [('Savings', 'Savings'), ('Current','Current')]
    account_type=models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='Savings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    def __str__(self):
        return str(f'{self.account_number} - {self.balance}')
    
    
class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) 
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    TRANSACTION_TYPES=[('Deposit', 'Deposit'),
                       ('Withdrawal','Withdrawal'),
                       ('Transfer_in', 'Transfer_in'),
                       ('Transfer_out', 'Transfer_out')]
    transaction_type=models.CharField(choices=TRANSACTION_TYPES, max_length=15)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    remarks = models.CharField(max_length=255, blank=True)  
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.transaction_id)

    