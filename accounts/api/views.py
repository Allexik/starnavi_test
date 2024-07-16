from rest_framework import viewsets, status
from rest_framework.response import Response

from common.permissions import IsOwner
from accounts.api.serializers import ProfileSerializer
from posts.models import Post


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwner]

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
