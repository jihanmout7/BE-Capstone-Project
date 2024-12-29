from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .models import Post
from .serializers import PostSerializer
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()


class PostListCreateView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        posts = Post.objects.all().order_by('-timestamp')  # Reverse chronological order
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create a new post
        user = self.get_authenticated_user(request)  # Getting the authenticated user

        # Ensure 'content' is in the request data
        content = request.data.get("content")
        if not content:
            return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user field automatically
        request.data["user"] = user.id  # Automatically associate the current user

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_authenticated_user(self, request):
        # Get JWT from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            # Decode the JWT token to get the user info
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding token.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        return user


class PostDetailView(APIView):
    def get(self, request, post_id):
        # Retrieve a specific post by its ID
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, post_id):
        # Update an existing post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the author of the post
        user = self.get_authenticated_user(request)
        if post.user != user:
            raise PermissionDenied("You are not the author of this post.")

        # Remove 'user' field from the data as it is unnecessary in PUT
        request.data['user'] = user.id  # Ensure the current user is the owner of the post

        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        # Delete a post
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the authenticated user is the author of the post
        user = self.get_authenticated_user(request)
        if post.user != user:
            raise PermissionDenied("You are not the author of this post.")

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get_authenticated_user(self, request):
        # Get JWT from the cookies
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            # Decode the JWT token to get the user info
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding token.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        return user
