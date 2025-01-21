from django.urls import path
from . import views
from .views import ProtectedView
from .views import register, assign_role, login_view, logout_view
# from .models import CustomUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/protected/', ProtectedView.as_view(), name='protected_view'),
    path('assign-role/', assign_role, name='assign_role'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
