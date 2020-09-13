from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from django.contrib.auth import get_user_model
from django.utils import timesince, timezone

from comma.models import Post, Category


class CategoryForPostSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, instance):
        return {
            'title': instance.title,
            'cat_url': instance.cat_url
        }

    class Meta:
        model = Category
        exclude = ['id', 'description', 'active', 'slug']


class UserInfoSerializer(serializers.ModelSerializer):
    # TODO: create account app to customize user profiles and add bio, img , ..
    class Meta:
        model = get_user_model()
        fields = ['username']


class PostListSerializer(TaggitSerializer, serializers.ModelSerializer):
    updated_at = serializers.SerializerMethodField()
    publish_at = serializers.SerializerMethodField()
    category = CategoryForPostSerializer()
    created_by = UserInfoSerializer()
    tags = TagListSerializerField()

    def get_updated_at(self, instance):
        return {
            'string': timesince.timesince(instance.updated_at, timezone.now()) + ' ago',
            'time-format': instance.updated_at
        }

    def get_publish_at(self, instance):
        return {
            'string': timesince.timesince(instance.publish_datetime, timezone.now()) + ' ago',
            'time-format': instance.publish_datetime
        }

    class Meta:
        model = Post
        exclude = ['created_at', 'active', 'publish_datetime']


class PostCreateSerializer(serializers.ModelSerializer):
    pass
