from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.views import Response

from common.permissions import IsOwnerOrReadOnly
from posts.api.serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='daily-breakdown')
    def daily_breakdown(self, request):
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        queryset = self.get_queryset()
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        queryset = queryset.values('created_at__date').annotate(
            comment_count=models.Count('id'),
            blocked_count=models.Count('blocked')
        ).order_by('-created_at__date')

        return Response(queryset)
