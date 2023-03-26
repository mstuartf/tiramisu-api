from django.urls import path

from . import views

urlpatterns = [
    path('oauth/callback/', views.oauth_callback, name="oauth_callback"),
    path('test/', views.test, name="test"),
]

app_name = "salesforce"
