import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework.reverse import reverse

from djoser import utils
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
def test_valid_user_activate(inactive_test_user):
    client = APIClient()
    response = client.post(
        path=reverse('user-activate'),
        data={
            'uid': utils.encode_uid(inactive_test_user.pk),
            'token': default_token_generator.make_token(inactive_test_user)
        })

    inactive_test_user.refresh_from_db()
    assert inactive_test_user.is_active is True
    assert response.status_code == status.HTTP_204_NO_CONTENT
