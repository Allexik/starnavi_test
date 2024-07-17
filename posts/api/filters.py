import django_filters

from posts.models import Post, Comment


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['title', 'content', 'date_from', 'date_to', 'blocked']


class CommentFilter(django_filters.FilterSet):
    content = django_filters.CharFilter(lookup_expr='icontains')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    post = django_filters.ModelChoiceFilter(queryset=Post.objects.all())
    replied_comment = django_filters.ModelChoiceFilter(queryset=Comment.objects.all())

    class Meta:
        model = Comment
        fields = ['post', 'replied_comment', 'content', 'date_from', 'date_to', 'auto_generated']
