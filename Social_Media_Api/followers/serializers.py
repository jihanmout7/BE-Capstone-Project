from rest_framework import serializers
from .models import Follow
from django.contrib.auth.models import User

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['follower', 'following', 'created_at']

    # Ensure that the follower is not the same as the following user
    def validate(self, attrs):
        if attrs['follower'] == attrs['following']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs
