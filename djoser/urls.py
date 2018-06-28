from django.conf.urls import include, url
from django.contrib.auth import get_user_model
import rest_framework

from rest_framework.routers import DefaultRouter, Route

from djoser import views

User = get_user_model()


def drf_compat(detail=False):
    drf_ver = tuple(int(i) for i in rest_framework.__version__.split('.'))
    if drf_ver >= (3, 8):
        return {'detail': detail}
    return {}


class DjoserRouter(DefaultRouter):
    def __init__(self, include_token_urls=False):
        super(DjoserRouter, self).__init__()
        self.trailing_slash = '/?'

        self._register_urls(include_token_urls)

    def _register_urls(self, include_token_urls):
        # if include_token_urls:
        self.register(
            r'tokens',
            views.TokenViewSet,
            base_name='token',
        )
        self.register(
            r'users',
            views.UsersViewSet,
            base_name='user'
        )
        self.register(
            r'password/update',
            views.PasswordUpdateViewSet,
            base_name='password-update',
        )
        self.register(
            r'password/reset',
            views.PasswordResetViewSet,
            base_name='password-reset',
        )
        self.register(
            r'password/confirm',
            views.PasswordResetConfirmViewSet,
            base_name='password-confirm',
        )

router = DjoserRouter()

urlpatterns = [
    url(r'', include(router.urls)),
]
