from rest_framework.routers import DefaultRouter
from django.urls import include, path

from views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

subscriptions = UserViewSet.as_view({'get': 'subscriptions', })

urlpatterns = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('router.urls')),
    path('', include('djoser.urls')),
]
