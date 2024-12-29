from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.contrib.auth import get_user_model
from .models import Follow
from .serializers import FollowSerializer
import jwt
from django.conf import settings

User = get_user_model()


class FollowView(APIView):
    def post(self, request):
        # Get authenticated user
        user = self.get_authenticated_user(request)

        # Get the user to follow from the request data
        following_user_id = request.data.get('following')  # ID of the user to follow
        if not following_user_id:
            return Response({"detail": "The 'following' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            following_user = User.objects.get(id=following_user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is not following themselves
        if user == following_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the follow relationship already exists
        if Follow.objects.filter(follower=user, following=following_user).exists():
            return Response({"detail": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the follow relationship
        follow = Follow.objects.create(follower=user, following=following_user)
        return Response(FollowSerializer(follow).data, status=status.HTTP_201_CREATED)

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


class UnfollowView(APIView):
    def post(self, request):
        # Get authenticated user
        user = self.get_authenticated_user(request)

        # Get the user to unfollow from the request data
        following_user_id = request.data.get('following')  # ID of the user to unfollow
        if not following_user_id:
            return Response({"detail": "The 'following' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            following_user = User.objects.get(id=following_user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the user is not unfollowing themselves
        if user == following_user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the follow relationship exists
        follow = Follow.objects.filter(follower=user, following=following_user).first()
        if not follow:
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the follow relationship
        follow.delete()
        return Response({"detail": "Unfollowed successfully."}, status=status.HTTP_204_NO_CONTENT)

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
