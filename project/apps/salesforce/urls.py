from django.urls import path

from . import views

urlpatterns = [
    path('oauth/callback/', views.oauth_callback, name="oauth_callback"),
]

app_name = "salesforce"
