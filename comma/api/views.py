from rest_framework import generics

from comma.models import Post
from comma.api import serializers


class PostListAPI(generics.ListAPIView):
    # TODO: if admin can see everything
    # TODO: Permission class
    queryset = Post.objects.filter(status__exact='PU', active__exact=True)
    serializer_class = serializers.PostListSerializer


class PostCreateAPI(generics.CreateAPIView):
    queryset = Post.objects.all()
