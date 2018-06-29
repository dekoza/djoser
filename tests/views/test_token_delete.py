import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
@pytest.mark.parametrize("trailing_slash", ['', '/'])
def test_valid_token_delete(test_user, settings, trailing_slash):
    from djoser.conf import settings as djoser_settings

    settings.DJOSER = dict(
        settings.DJOSER,
        **{'TOKEN_MODEL': 'rest_framework.authtoken.models.Token'}
    )
    token, _ = djoser_settings.TOKEN_MODEL.objects.get_or_create(
        user=test_user
    )
    assert djoser_settings.TOKEN_MODEL.objects.count() == 1

    client = APIClient()
    client.force_login(test_user)
    response = client.delete(
        reverse('token-detail', kwargs=dict(pk=token.pk)) + trailing_slash
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert djoser_settings.TOKEN_MODEL.objects.count() == 0
