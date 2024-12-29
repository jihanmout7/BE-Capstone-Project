from django.urls import path
from .views import FeedView

urlpatterns = [
    path('feeds/', FeedView.as_view()),

]
