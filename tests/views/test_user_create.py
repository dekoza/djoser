import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
def test_valid_user_create():
    client = APIClient()
    response = client.post(
        reverse('user-list'),
        data={
            User.USERNAME_FIELD: 'test@localhost',
            'password': 'testing123',
        })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {User.USERNAME_FIELD: 'test@localhost', 'id': 1}
