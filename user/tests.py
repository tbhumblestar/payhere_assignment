from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken


CREATE_USER_URL = reverse("user:user_create")
GET_TOKEN_URL = reverse("user:get_token")
REFRESH_TOKEN_URL = reverse("user:refresh_token")


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_token(user):
    data = {}
    refresh = RefreshToken.for_user(user)
    
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token,refresh_token


class PublicUserAPITests(TestCase):
    """Test as not authenticated user"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }

        res = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertIn("email", res.data)

    def test_user_with_email_exists_error(self):
        """Error returned if user email already exists"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**data)
        res = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_jwt_token_success(self):
        """Test get token when user login."""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }

        create_user(**data)
        res = self.client.post(GET_TOKEN_URL, data)

        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertIn("email", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_jwt_token_wrong_password_error(self):
        """test error returns by worng password login"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        
        create_user(**data)
        wrong_data = {
            "email": "test@example.com",
            "password": "wrong_password",
        }
        res = self.client.post(GET_TOKEN_URL, wrong_data)
        
        self.assertNotIn('access',res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_token_email_not_exist_error(self):
        """Test error returned if email not exist."""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        
        create_user(**data)
        wrong_data = {
            "email": "wrong_test@example.com",
            "password": "testpass123",
        }
        res = self.client.post(GET_TOKEN_URL, wrong_data)
        
        self.assertNotIn('access',res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_refresh_access_token_success(self):
        """Refresh access_token success"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }

        user = create_user(**data)
        access_toekn, refresh_token = create_token(user)

        token_data = {
            'refresh' : refresh_token
        }

        res = self.client.post(REFRESH_TOKEN_URL, token_data)

        self.assertIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_refresh_access_token_fail(self):
        """Refresh access_token fail by wrong refresh token"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }

        user = create_user(**data)
        access_toekn, refresh_token = create_token(user)

        wrong_refresh_token = refresh_token + 'wrong'

        token_data = {
            'refresh' : wrong_refresh_token
        }

        res = self.client.post(REFRESH_TOKEN_URL, token_data)

        self.assertNotIn("access", res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)