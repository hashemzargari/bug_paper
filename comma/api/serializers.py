from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils import timesince, timezone

from comma.models import Post, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserInfoSerializer(serializers.ModelSerializer):
    # TODO: create account app to customize user profiles and add bio, img , ..
    class Meta:
        model = get_user_model()
        fields = ['username']


class PostListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    created_by = UserInfoSerializer()
    updated_at = serializers.SerializerMethodField()
    publish_at = serializers.SerializerMethodField()

    def get_updated_at(self, instance):
        return {
            'string': timesince.timesince(instance.updated_at, timezone.now()),
            'time-format': instance.updated_at
        }

    def get_publish_at(self, instance):
        return {
            'string': timesince.timesince(instance.publish_datetime, timezone.now()),
            'time-format': instance.publish_datetime
        }

    class Meta:
        model = Post
        exclude = ['created_at', 'active', 'publish_datetime']


class PostCreateSerializer(serializers.ModelSerializer):
    pass
