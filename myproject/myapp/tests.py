from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_user_profile(self):
        url = reverse('user-profile-create')
        data = {
            'first_name': 'Mohana',
            'last_name': 'Prasad',
            'email': 'MohanaPrasad@example.com'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.first().user, self.user)
        self.assertEqual(UserProfile.objects.first().first_name, 'Mohana')
        self.assertEqual(UserProfile.objects.first().last_name, 'Prasad')
        self.assertEqual(UserProfile.objects.first().email, 'MohanaPrasad@example.com')

    def test_update_user_profile(self):
        user_profile = UserProfile.objects.create(user=self.user, first_name='Mohana', last_name='Prasad', email='MohanaPrasad@example.com')

        url = reverse('user-profile-update', args=[user_profile.id])
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_profile.refresh_from_db()
        self.assertEqual(user_profile.first_name, 'Updated')
        self.assertEqual(user_profile.last_name, 'User')
        self.assertEqual(user_profile.email, 'updateduser@example.com')