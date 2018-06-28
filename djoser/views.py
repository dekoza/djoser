from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import list_route, permission_classes as permclasses
from rest_framework.response import Response

from djoser.conf import settings

User = get_user_model()


def run_pipeline(request, steps):
    return settings.VIEW_PIPELINE_ADAPTER(request, steps)


class UsersViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action in ['create', 'activate']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @permclasses([permissions.AllowAny])
    def create(self, request, *args, **kwargs):
        steps = settings.PIPELINES['user_create']
        response_data = run_pipeline(request, steps)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        # TODO: this should allow to get a particular user
        steps = settings.PIPELINES['user_detail']
        response_data = run_pipeline(request, steps)
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        steps = settings.PIPELINES['user_update']
        response_data = run_pipeline(request, steps)
        return Response(response_data, status=status.HTTP_200_OK)

    def partial_update(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        steps = settings.PIPELINES['user_delete']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['GET', 'DELETE'])
    def me(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    @list_route(methods=['POST'])
    def change_username(self, request, *args, **kwargs):
        steps = settings.PIPELINES['username_update']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['POST'])
    def activate(self, request, *args, **kwargs):
        steps = settings.PIPELINES['user_activate']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        steps = settings.PIPELINES['password_update']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        steps = settings.PIPELINES['password_reset']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetConfirmViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        steps = settings.PIPELINES['password_reset_confirm']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        steps = settings.PIPELINES['token_create']
        response_data = run_pipeline(request, steps)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        steps = settings.PIPELINES['token_delete']
        run_pipeline(request, steps)
        return Response(status=status.HTTP_204_NO_CONTENT)
