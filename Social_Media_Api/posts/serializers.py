from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # Make sure the user field is read-only since we get it from the authenticated user
    def validate_user(self, value):
        # We can optionally validate the user here if needed
        return value
