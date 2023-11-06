from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.CustomUserViewSet, basename="user")



urlpatterns = [
    path('auth/', include(router.urls)),
    path('auth/admin/', views.AdminListCreateView().as_view()),
    path('auth/login/', views.user_login, name="login_view"),
    path('auth/reset-password/verify/', views.reset_password_otp_verification),
    path("auth/logout/", views.logout_view, name="logout_view"),
    path('auth/otp/verify/', views.otp_verification),
    path('auth/otp/new/', views.reset_otp),
    path('auth/fcm-token/', views.update_firebase_token),
    path("permissions/", views.PermissionList.as_view(), name="permissions"),
    path("activity-logs/", views.activity_logs),
    path("auth/image-upload", views.image_upload, name="image-upload"),
]
