from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
import jwt
import datetime
from django.conf import settings

# Get the user model
User = get_user_model()

# Helper function to decode JWT and retrieve user
def get_user_from_token(token):
    try:
        # Decode the JWT token using the secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['id'])
        return user
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except User.DoesNotExist:
        raise AuthenticationFailed('User does not exist')

# Register view to create a new user
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Login view to authenticate and generate JWT token
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Retrieve the user by email
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        # Check if the password is correct
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Create JWT payload
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Encode the token
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response()

        # Set the token in a cookie (optional)
        response.set_cookie(key='jwt', value=token, httponly=True)

        # Return the token in response (for testing purposes)
        response.data = {'jwt': token}
        return response

# View to get the currently authenticated user
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            # Decode the JWT token and retrieve the user
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        # Retrieve user based on the decoded payload
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Logout view to delete JWT token (cookie)
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'success'}
        return response

# Update user profile (requires authentication)
class UpdateUserProfileView(APIView):


    def patch(self, request):
        # Get the token from the cookie or Authorization header
        token = request.COOKIES.get('jwt')  # Try getting JWT from cookie
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        # Decode the token and get the user
        user = get_user_from_token(token)

        # Proceed with profile update
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class DeleteUserView(APIView):
    def delete(self, request, *args, **kwargs):
        # Get the JWT token from the cookies
        token = request.COOKIES.get('jwt')  # Try getting JWT from cookie
        if not token:
            raise AuthenticationFailed('Authentication credentials were not provided.')

        try:
            # Decode the JWT token to extract user information
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Retrieve the user based on the payload's user ID
            user = User.objects.get(id=payload['id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        # Proceed with deleting the user
        user.delete()

        return Response({"message": "User deleted successfully."}, status=204)