from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating user with an email successful"""
        email = "test@email.com"
        password = "tes123"
        user = User.objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test email for a new user is normalized"""
        email = "test@LONDON.COM"
        user = User.objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_Email(self):
        """Test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            User.objects.create_user(None, 'test123')

    def test_create_new_super_user(self):
        """Tes creating new super user"""
        user = User.objects.create_superuser(
            'admin@email.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
