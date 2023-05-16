from django.db import models
from django.contrib.auth.models import User
import uuid


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nominal_value = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    ip_address = models.GenericIPAddressField(editable=False)
    request_date = models.DateTimeField(auto_now_add=True)
    bank = models.CharField(max_length=200)
    client = models.ForeignKey(User, on_delete=models.CASCADE)

    def outstanding_balance(self):
        payments = self.payment_set.all()
        total_paid = sum(payment.payment_value for payment in payments)
        balance = self.nominal_value - total_paid
        return balance if balance > 0 else 0


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_value = models.DecimalField(max_digits=15, decimal_places=2)