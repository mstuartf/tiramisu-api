from django.urls import path
from . import views

urlpatterns = [
    path('signup/success', views.signup_success_view, name="signup_success"),
    path('signup/', views.signup_view, name="signup"),
    path('signup/<company_id>/', views.join_account_view, name="join_account"),
]

app_name = "accounts"
