from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.UserView, basename='users')

urlpatterns = [
    path('signup/success', views.signup_success_view, name="signup_success"),
    path('signup/', views.signup_view, name="signup"),
    path('signup/<company_id>/', views.join_account_view, name="join_account"),
    path('users/', include(router.urls)),
]

app_name = "accounts"
