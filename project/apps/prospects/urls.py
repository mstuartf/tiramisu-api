from . import views
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
# todo: REMOVE_V1
router.register('', views.ProspectView, basename='prospects')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "prospects"
