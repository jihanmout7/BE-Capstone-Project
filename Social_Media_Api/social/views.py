from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # Use AuthenticationForm for login
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("Home:page")  # Redirect to the homepage after successful registration
    else:
        form = UserCreationForm()  # Initialize form for GET request
    
    return render(request, "social/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Use AuthenticationForm for login
        if form.is_valid():
            user = form.get_user()  # Get the user from the form
            login(request, user)  # Log the user in
            return redirect("Home:page")  # Redirect to the homepage after successful login
    else:
        form = AuthenticationForm()  # Initialize form for GET request

    return render(request, "social/login.html", {"form": form})



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

    def get(self, request):
        return Response({"message": "This is a protected resource!"})
