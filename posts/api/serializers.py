from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'blocked',)

    def update(self, instance, validated_data):
        validated_data.pop('post', None)
        validated_data.pop('answer_to', None)
        return super().update(instance, validated_data)
