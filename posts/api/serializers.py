from rest_framework import serializers

from posts.models import Post, Comment
from posts.services import check_text_inappropriateness


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)

    def validate_title(self, title):
        if check_text_inappropriateness(title):
            raise serializers.ValidationError('Title is inappropriate')
        return title

    def validate_content(self, content):
        if check_text_inappropriateness(content):
            raise serializers.ValidationError('Content is inappropriate')
        return content


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)

    def validate_content(self, content):
        if check_text_inappropriateness(content):
            raise serializers.ValidationError('Content is inappropriate')
        return content

    def update(self, instance, validated_data):
        validated_data.pop('post', None)
        validated_data.pop('answer_to', None)
        return super().update(instance, validated_data)
