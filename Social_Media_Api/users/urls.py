from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, UpdateUserProfileView, DeleteUserView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),        # User registration
    path('login', LoginView.as_view(), name='login'),                  # User login
    path('user', UserView.as_view(), name='user'),                     # Get user profile
    path('logout', LogoutView.as_view(), name='logout'),               # User logout
    path('user/update/', UpdateUserProfileView.as_view(), name='update_user_profile'),  # Update user profile
    path('user/delete/', DeleteUserView.as_view(), name='delete_user'), # Delete user account
]
