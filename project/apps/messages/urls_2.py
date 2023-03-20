from django.urls import include, path
from rest_framework import routers

from . import views_2

router = routers.DefaultRouter()
router.register(r'sets', views_2.MessageSetView, basename='message_sets')

urlpatterns = [
    path(r'', include(router.urls)),
]

app_name = "message_sets_2"

