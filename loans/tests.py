import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Loan, Payment

class LoanTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='usertest', password='user123456')
        self.superuser = User.objects.create_superuser(username='admintest', password='admin123456')
        self.loan_data = {
            'nominal_value': 1000.0,
            'interest_rate': 0.05,
            'ip_address': '127.0.0.1',  # Defina um valor para o campo ip_address
            'bank': 'Banco Teste'
        }
        self.payment_data = {
            'payment_value': 500.0
        }
        self.token_user = str(RefreshToken.for_user(self.user).access_token)
        self.token_superuser = str(RefreshToken.for_user(self.superuser).access_token)

    # Loans - user
    def test_create_and_read_loan_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        # Create Loan
        response = self.client.post('/loans/', data=self.loan_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(Loan.objects.first().client, self.user)

        # Read
        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client']['username'], self.user.username)

    def test_update_loan_by_user(self):
        loan = Loan.objects.create(client=self.user, **self.loan_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        new_bank = 'Banco Y'
        data = {'bank': new_bank}
        response = self.client.patch(f'/loans/{loan.id}/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        loan.refresh_from_db()
        self.assertNotEqual(loan.bank, new_bank)

    def test_delete_loan_by_user(self):
        loan = Loan.objects.create(client=self.user, **self.loan_data)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_user)
        response = self.client.delete(f'/loans/{loan.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Loan.objects.count(), 1)

    # Loans - superuser
    def test_loan_by_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token_superuser)

        # Create
        response = self.client.post('/loans/', data=self.loan_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Loan.objects.count(), 1)
        self.assertEqual(Loan.objects.first().client, self.superuser)

        # Read
        response = self.client.get('/loans/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        # Update
        loan = Loan.objects.first()  
        new_bank = 'Banco Y'
        data = {'bank': new_bank}
        response = self.client.patch(f'/loans/{loan.id}/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertEqual(loan.bank, new_bank)

        # Delete
        response = self.client.delete(f'/loans/{loan.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Loan.objects.count(), 0)


    # Payments - user
    # Payments - superuser