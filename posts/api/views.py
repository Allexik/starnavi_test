from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import Response
from django_filters import rest_framework as filters

from common.permissions import IsOwnerOrReadOnly
from posts.api.serializers import PostSerializer, CommentSerializer
from posts.api.filters import PostFilter, CommentFilter
from posts.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PostFilter

    def get_queryset(self):
        return super().get_queryset().filter(blocked=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_queryset(self, include_blocked=False):
        if include_blocked:
            return super().get_queryset()
        return super().get_queryset().filter(blocked=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="daily-breakdown")
    def daily_breakdown(self, request):
        queryset = (
            self.get_queryset(include_blocked=True)
            .values("created_at__date")
            .annotate(
                comment_count=models.Count("id"),
                blocked_count=models.Count(
                    models.Case(models.When(blocked=True, then=1))
                ),
            )
            .order_by("-created_at__date")
        )

        return Response(queryset)
