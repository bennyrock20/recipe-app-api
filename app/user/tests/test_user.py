from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from rest_framework import status

User = get_user_model()

CREATE_USER_URL = reverse('user:create')
TOKE_URL = reverse('user:token')


def create_user(**params):
    return User.objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the user api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': "email@email.com",
            'password': 'setup123',
            'name': "Test Name"
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': "email@email.com",
            'password': "12398908908"
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that  the password must be more than 5 characters"""
        payload = {'email': 'thisisaemails@email.com', 'password': '123', 'name': 'wilian'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(email=payload['email']).exists()

        self.assertFalse(user_exists)

    def test_create_user_for_user(self):
        """Test taht a token is created for the user"""
        payload = {'email': 'test@mail.com', 'password': 'setup1235', 'name': 'name'}
        create_user(**payload)
        res = self.client.post(TOKE_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test taht token is not created if invalid credentials"""
        create_user(email="test@em.com", password='mysecurepassword')
        payload = {'email': 'test@em.com', 'password': 'wronpassword', 'name': 'Wilian'}
        res = self.client.post(TOKE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exists """
        payload = {'email': 'test@london.com', 'password': 'qwrqwer45'}

        res = self.client.post(TOKE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password  are required"""
        payload = {'email': 'demo@email.com', 'password': ''}

        res = self.client.post(TOKE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'email': '', 'password': 'thisisapassword'}

        res = self.client.post(TOKE_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)