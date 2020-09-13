from django.urls import path
from comma.api.views import PostListAPI

urlpatterns = [
    path('', PostListAPI.as_view(), name='post-list-create')
]
