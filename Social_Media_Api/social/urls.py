from django.urls import path
from . import views
from .views import ProtectedView
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    # Other URL patterns...
]



urlpatterns = [
    # Other URL patterns...
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]




urlpatterns = [
    # Other URL patterns...
    path('protected/', ProtectedView.as_view(), name='protected'),
]
