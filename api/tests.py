from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class TestAuth(TestCase):
    def test_login(self):
        login = 'admin'
        password = 'pass'
        User.objects.create_user(
            username=login,
            email='admin@example.com',
            password=password,
        ).save()
        response = self.client.post('/api/token/', data={'username': login, 'password': password})

        self.assertEqual(response.status_code, 200, response.content)
        response = response.json()
        self.assertIn('access', response)
        self.assertIn('refresh', response)
        token = response['access']

        response = self.client.get('/api/profile/', HTTP_AUTHORIZATION='Bearer aoe')
        self.assertEqual(response.status_code, 401, response.content)

        response = self.client.get('/api/profile/', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, 200, response.content)
