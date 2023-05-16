from rest_framework import serializers

from ..models import Loan, Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class LoanSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'nominal_value', 'interest_rate', 'ip_address', 'request_date', 'bank', 'client', 'outstanding_balance']
        read_only_fields = ['id', 'ip_address', 'request_date', 'client', 'outstanding_balance']

    def get_outstanding_balance(self, obj):
        payments = Payment.objects.filter(loan=obj)
        total_payments = sum(payment.payment_value for payment in payments)
        outstanding_balance = obj.nominal_value - total_payments
        return outstanding_balance


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'loan', 'payment_date', 'payment_value']
        read_only_fields = ['id', 'payment_date']