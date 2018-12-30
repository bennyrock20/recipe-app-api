from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email="admin@email.com",
            password="s34rfwe"
        )
        self.client.force_login(self.admin_user)

        self.user = User.objects.create_user(
            email="test@email.com",
            password="setup123",
            name="Test Full User name",
        )

    def test_user_loggedin(self):
        """Check if user is logged in"""
        self.assertIn('_auth_user_id', self.client.session)

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')

        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)


    def test_user_add_page(self):
        """Test user add page"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code,200)

