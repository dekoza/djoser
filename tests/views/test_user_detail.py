import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize("trailing_slash", ['', '/'])
def test_valid_user_detail(test_user, trailing_slash):
    client = APIClient()
    client.force_login(test_user)
    response = client.get(reverse('user-me') + trailing_slash)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        User.USERNAME_FIELD: 'test',
        User.get_email_field_name(): 'test@localhost',
        'id': 1,
    }
