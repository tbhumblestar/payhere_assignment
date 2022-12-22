from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from record.models import Record


CREATE_USER_URL = reverse("user:user_create")
GET_TOKEN_URL = reverse("user:get_token")
REFRESH_TOKEN_URL = reverse("user:refresh_token")
RECORD_URL = reverse('record:record')

def record_detail_url(record_id):
    """Create and return a record detail URL."""
    return reverse('record-detail', args=[record_id])

def create_record(user, **params):
    """Create and return record object."""
    data = {
        "money":10000,
        "detail_info":"test"
    }
    data.update(params)

    record = Record.objects.create(user=user, **params)
    return record


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

def create_token(user):
    data = {}
    refresh = RefreshToken.for_user(user)

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token


class PublicRecordAPITests(TestCase):
    """Test as not authenticated user"""

    def setUp(self):
        self.client = APIClient()
        
    def test_unauth_required_error(self):
        """Test return error as unauthenticted_user."""

        res = self.client.get(RECORD_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecordApiTests(TestCase):
    """Test Record API requests as authenticated user."""
    
    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)