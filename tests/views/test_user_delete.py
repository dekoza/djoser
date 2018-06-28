import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db(transaction=False)
def test_valid_user_delete(test_user):
    client = APIClient()
    client.force_login(test_user)
    response = client.delete(
        reverse('user-detail', kwargs=dict(pk=test_user.pk)),
        {'current_password': 'testing123'}, format='json'
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 0
