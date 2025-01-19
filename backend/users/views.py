from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .decorators import role_required



from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'This is a protected endpoint!'})


# Admin-only view
@role_required(['admin'])
def admin_only_view(request):
    return JsonResponse({'message': 'Welcome, Admin!'})


@csrf_exempt
def register(request):
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     username = data['username']
    #     password = data['password']
    #     role = data.get('role', 'guest')
    #     if CustomUser.objects.filter(username=username).exists():
    #         return JsonResponse({'error': 'User already exists'}, status=400)
    #     user = CustomUser.objects.create_user(username=username, password=password, role=role)
    #     return JsonResponse({'message': 'User registered successfully'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Username and password are required'}, status=400)
            
            # Check if user already exists
            if user.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken'}, status=400)

            # Create the user
            user = user.objects.create_user(username=username, password=password)
            return JsonResponse({'message': f'User {user.username} registered successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method. Only POST is allowed.'}, status=405)


@csrf_exempt
def login_view(request):
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
