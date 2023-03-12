from . import views
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.PromptView, basename='prompts')

urlpatterns = [
    path(r'', include(router.urls)),
]

app_name = "prompts"
