from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from accounts.models import Profile


User = get_user_model()


class TestProfileViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)

    def test_profile_was_created(self):
        self.assertTrue(Profile.objects.exists())

    def test_profile_was_deleted(self):
        self.user.delete()
        self.staff_user.delete()
        self.assertFalse(Profile.objects.exists())
