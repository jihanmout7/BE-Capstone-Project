from django.urls import path
from .views import FollowView, UnfollowView

urlpatterns = [
    path('follow/', FollowView.as_view(), name='follow'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
]
