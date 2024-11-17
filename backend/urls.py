from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from authentication.viewset import AuthenticationViewSet
from users.viewset import UserViewSet

router = routers.DefaultRouter()
router.register(r'auth', AuthenticationViewSet, basename='authentication')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include(router.urls)),
    path('rest-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
