from rest_framework import serializers

from posts.models import Post, Comment
from posts.services import check_text_inappropriateness
from posts.tasks import answer_comment
from starnavi_test import settings


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)

    def validate(self, attrs):
        if settings.USE_MODERATION and ('content' in attrs or 'title' in attrs):
            list_of_texts = []
            if 'title' in attrs:
                list_of_texts.append(attrs['title'])
            if 'content' in attrs:
                list_of_texts.append(attrs['content'])
            text_to_check = '; '.join(list_of_texts)
            attrs['blocked'] = check_text_inappropriateness(text_to_check)
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)

    def validate(self, attrs):
        if settings.USE_MODERATION and 'content' in attrs:
            attrs['blocked'] = check_text_inappropriateness(attrs['content'])
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('post', None)
        validated_data.pop('answer_to', None)
        return super().update(instance, validated_data)

    def create(self, validated_data):
        instance = super().create(validated_data)

        if (
            not instance.blocked and
            instance.post.user.profile.auto_response and
            instance.post.user_id != instance.user_id
        ):
            answer_comment.apply_async((
                instance.id, instance.post.title, instance.post.content, instance.content
            ), countdown=instance.post.user.profile.auto_response_delay)

        return instance
