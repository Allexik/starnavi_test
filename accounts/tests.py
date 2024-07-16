from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from accounts.models import Profile


class TestProfileViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_was_created(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
