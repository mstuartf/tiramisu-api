from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'sets', views.MessageSetView, basename='message_sets')

urlpatterns = [
    path(r'', include(router.urls)),
]

app_name = "message_sets"
