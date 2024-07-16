from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

from accounts.models import Profile


User = get_user_model()


class TestProfileViewSet(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)

    def test_profile_was_created(self):
        self.assertTrue(Profile.objects.exists())

    def test_list_non_staff_user(self):
        url = reverse('profile-list')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_staff_user(self):
        url = reverse('profile-list')
        self.client.login(username='staffuser', password='staffpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_was_deleted(self):
        self.user.delete()
        self.staff_user.delete()
        self.assertFalse(Profile.objects.exists())
