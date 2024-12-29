from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post  # Assuming the Post model is in the 'posts' app

User = get_user_model()

class Feed_of_posts(models.Model):
    user = models.ForeignKey(User, related_name='feeds', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='feeds', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feed of {self.user.username} on {self.timestamp}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like on {self.post.content} by {self.user.username}"
