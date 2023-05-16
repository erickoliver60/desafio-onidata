from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Loan, Payment
from .serializers import LoanSerializer, PaymentSerializer


class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer

    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(client=user)
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user, ip_address=self.request.META['REMOTE_ADDR'])

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        response = {'message': 'Update operation is not allowed'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        response = {'message': 'Delete operation is not allowed'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(loan__client=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        response = {'message': 'Update operation is not allowed'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        response = {'message': 'Delete operation is not allowed'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)