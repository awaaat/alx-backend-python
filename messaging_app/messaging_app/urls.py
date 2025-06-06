from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenRefreshView
from chats.auth import CustomTokenObtainPairView
from chats.views import UserViewSet, get_me  # 👈 get_me returns current user
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="ALX Messaging App API",
        default_version='v1',
        description="Detailed API documentation for internal and external use.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger/OpenAPI endpoints
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Chat app endpoints
    path('api/chats/', include('chats.urls')),

    # DRF login/logout UI
    path('api-auth/', include('rest_framework.urls')),

    # JWT Authentication
    path('api/token/', CustomTokenObtainPairView.as_view(), name='obtain-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # User endpoints
    path('api/users/me/', get_me, name='user-me'),  # 👈 current user info
    path('api/user/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
