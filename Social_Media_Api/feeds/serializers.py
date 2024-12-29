from rest_framework import serializers
from .models import Post

class Feed_of_postsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'timestamp']  # Include the fields you want in the response
