from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json
from .decorators import role_required
from rest_framework.decorators import permission_classes



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework import status



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected endpoint!'})


# Admin-only view
@role_required(['admin'])
def admin_only_view(request):
    return JsonResponse({'message': 'Welcome, Admin!'})


@api_view(['POST'])
def register(request):
    """
    API endpoint to register a new user.
    Example Request Body:
    {
        "username": "john_doe",
        "password": "securepassword",
        "email": "john@example.com"
    }
    """
    data = request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return Response({'error': 'All fields (username, password, email) are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user
    user = CustomUser.objects.create_user(username=username, email=email, password=password)

    # Assign default "Regular User" group
    regular_user_group, created = Group.objects.get_or_create(name='Regular User')
    user.groups.add(regular_user_group)

    return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@role_required(['admin'])  # Only Admins can assign roles
def assign_role(request):
    """
    API endpoint to assign a role to a user.
    Example Request Body:
    {
        "username": "john_doe",
        "role": "Admin"
    }
    """
    data = request.data
    username = data.get('username')
    role = data.get('role')

    if not username or not role:
        return Response({'error': 'Both username and role are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        group, created = Group.objects.get_or_create(name=role)
        user.groups.clear()  # Clear existing roles
        user.groups.add(group)
        return Response({'message': f'Role {role} assigned to {username} successfully!'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
def login_view(request):
    print('Request received:', request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'})
