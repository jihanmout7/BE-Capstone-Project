from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .models import Post
from followers.models import Follow
from .serializers import Feed_of_postsSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from django.db.models import Count

User = get_user_model()


class FeedView(APIView):
    serializer_class = Feed_of_postsSerializer

    class FeedPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 100

    def get(self, request):
        """
        Returns posts from users that the authenticated user follows, with sorting and pagination.
        """
        user = self.get_authenticated_user(request)

        # Fetch followed users
        followed_users = Follow.objects.filter(follower=user).values_list('following', flat=True)

        # Get the posts from followed users
        posts = Post.objects.filter(user__in=followed_users)

        # Sorting by query parameter (default to date if no parameter)
        sort_by = request.query_params.get('sort', 'date')  # Default to 'date' if no sort param is provided

        if sort_by == 'date':
            posts = posts.order_by('-timestamp')  # Sort by date (newest first)
        elif sort_by == 'popularity':
            posts = posts.annotate(like_count=Count('like')).order_by('-like_count')  # Sort by popularity (likes)
        else:
            posts = posts.order_by('-timestamp')  # Fallback to date if an invalid sort option is passed

        # Pagination
        paginator = self.FeedPagination()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = Feed_of_postsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_authenticated_user(self, request):
        """
        Decodes JWT token and retrieves the user object.
        """
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
