from . import views
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.MessageSetView, basename='message_sets')

urlpatterns = [
    path(r'', include(router.urls)),
]

app_name = "message_sets"
