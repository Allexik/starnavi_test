from rest_framework import serializers
from djoser.serializers import UserSerializer as DjoserUserSerializer

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('id', 'user',)


class CurrentUserSerializer(DjoserUserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + ('profile',)
