import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize("trailing_slash", ['', '/'])
def test_valid_username_update(test_user, trailing_slash):
    client = APIClient()
    client.force_login(test_user)
    response = client.post(
        reverse('user-change-username') + trailing_slash,
        {User.USERNAME_FIELD: 'test-new', 'current_password': 'testing123'}
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize("trailing_slash", ['', '/'])
def test_invalid_username_update_wrong_password(test_user, trailing_slash):
    client = APIClient()
    client.force_login(test_user)
    response = client.post(
        reverse('user-change-username') + trailing_slash,
        {User.USERNAME_FIELD: 'test-new', 'current_password': 'invalid'}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
