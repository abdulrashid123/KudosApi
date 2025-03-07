from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework import status
from kudos_app.models import Organization, UserProfile, Kudos


class KudosAPITestCase(APITestCase):
    """
    Test cases for Kudos API endpoints.
    """

    def setUp(self):
        """
        Set up test data including users, organizations, and profiles.
        """
        self.organization = Organization.objects.create(name="Test Org")
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        self.profile1 = UserProfile.objects.create(user=self.user1, organization=self.organization)
        self.profile2 = UserProfile.objects.create(user=self.user2, organization=self.organization)
        self.access_token = str(RefreshToken.for_user(self.user1).access_token)

    def authenticate(self):
        """
        Authenticate requests using JWT token.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """
        response = self.client.post("/api/token/", {"username": "user1", "password": "testpass"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        """
        Test login failure with incorrect password.
        """
        response = self.client.post("/api/token/", {"username": "user1", "password": "wrongpass"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        """
        Test retrieving the user profile after authentication.
        """
        self.authenticate()
        response = self.client.get("/kudos/get-user-profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("organization", response.data[0])
        self.assertIn("username", response.data[0])

    def test_kudos_creation(self):
        """
        Test giving Kudos to another user successfully.
        """
        self.authenticate()
        data = {"giver": self.user1.id, "receiver": self.user2.id, "message": "Great work!"}
        response = self.client.post("/kudos/create-kudos/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        kudos = Kudos.objects.first()
        self.assertEqual(kudos.giver, self.user1)
        self.assertEqual(kudos.receiver, self.user2)
        self.assertEqual(kudos.message, "Great work!")

    def test_kudos_limit(self):
        """
        Test that a user cannot give Kudos if they have no remaining Kudos.
        """
        self.profile1.kudos_remaining = 0
        self.profile1.save()
        self.authenticate()
        data = {"giver": self.user1.id, "receiver": self.user2.id, "message": "Nice job!"}
        response = self.client.post("/kudos/create-kudos/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Kudos Not remaining")
