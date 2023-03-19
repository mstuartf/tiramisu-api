from . import views
from django.urls import include, path

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'sections/types', views.TemplateSectionTypeView, basename='template_section_types')
router.register(r'styles', views.TemplateStyleView, basename='template_styles')
router.register(r'', views.TemplateView, basename='templates')

urlpatterns = [
    path(r'', include(router.urls)),
]

app_name = "templates"
