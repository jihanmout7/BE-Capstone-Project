from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class Post(models.Model):
    content = models.TextField()  # Content of the post
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # The user who created the post
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created

    def __str__(self):
        return f"Post by {self.user.username} on {self.timestamp}"
