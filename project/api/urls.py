from django.contrib import admin
from django.urls import path, include
from .views import health_check
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health-check", health_check),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("accounts/", include("apps.accounts.urls")),
    path("prompts/", include("apps.prompts.urls")),
    path("prospects/", include("apps.prospects.urls")),
]
