from django.urls import path
from .views import SpotifyAPIView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet, basename="users")

urlpatterns = [
  path('spotify/<int:pk>/', SpotifyAPIView.as_view(), name="spotify")
]

urlpatterns += router.urls