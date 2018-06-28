import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
def test_valid_password_update(test_user):
    client = APIClient()
    client.force_login(test_user)
    response = client.post(
        path=reverse('password-update-list'),
        data={
            'current_password': 'testing123',
            'new_password': 'new-password123'
        }
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
