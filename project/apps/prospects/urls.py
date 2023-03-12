from . import views
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('', views.ProspectView, basename='prospects')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = "prospects"
