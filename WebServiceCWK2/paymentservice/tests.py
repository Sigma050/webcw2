from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import User, Order


class PaymentServiceTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'Name': 'test_user',
            'Email': 'test_user@example.com',
            'Password': 'test_password',
        }
        self.url_register = reverse('register')
        self.url_login = reverse('login')
        self.url_order = reverse('order')
        self.url_pay = reverse('pay')

    def test_register_user(self):
        response = self.client.post(
            self.url_register,
            data=self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Name'], 'test_user')

    def test_login_user(self):
        user_data = {
            'ID': self.user.id,
            'Password': 'test_password',
        }
        response = self.client.post(
            self.url_login,
            data=user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'success')

    def test_create_order(self):
        order_data = {
            'MerchantOrderId': '123',
            'Price': 100,
        }
        response = self.client.post(
            self.url_order,
            data=order_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('PaymentId' in response.data)
        self.assertTrue('Stamp' in response.data)

    def test_pay_order(self):
        from_account = get_user_model().objects.create_user(username='test_from_user', email='test_from_user@example.com', password='test_password')
        from_account.balance = 1000
        from_account.save()
        order = Order.objects.create(merchant_order_id='123', order_time=datetime.now(), price=500, stamp='stamp', to_account=self.user.id)
        pay_data = {
            'PaymentId': order.id,
        }
        self.client.force_authenticate(user=from_account)
        response = self.client.post(
            self.url_pay,
            data=pay_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Stamp' in response.data)
        order.refresh_from_db()
        from_account.refresh_from_db()
        to_account = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(order.payment_time.date(), datetime.today().date())
        self.assertEqual(from_account.balance, 500)
        self.assertEqual(to_account.balance, 500)
