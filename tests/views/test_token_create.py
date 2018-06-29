import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize("trailing_slash", ['', '/'])
def test_valid_token_create(test_user, settings, trailing_slash):
    from djoser.conf import settings as djoser_settings

    settings.DJOSER = dict(
        settings.DJOSER,
        **{'TOKEN_MODEL': 'rest_framework.authtoken.models.Token'}
    )
    token_model = djoser_settings.TOKEN_MODEL
    djoser_settings.SERIALIZERS['token'].Meta.model = token_model

    client = APIClient()
    response = client.post(reverse('token-list') + trailing_slash, {
        User.USERNAME_FIELD: 'test',
        'password': 'testing123',
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {'token': test_user.auth_token.key}
