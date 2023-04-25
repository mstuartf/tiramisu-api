from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'sets', views.MessageSetView, basename='message_sets')
router.register(r'linkedin', views.LinkedInMessageView, basename='linkedin_msgs')
router.register(r'linkedin/like', views.LinkedInLikeView, basename='linkedin_likes')
router.register(r'linkedin/comment', views.LinkedInCommentView, basename='linkedin_comments')

urlpatterns = [
    path('activity/<company_id>', views.activity_view, name="activity_view"),
    path(r'', include(router.urls)),
]

app_name = "message_sets"
