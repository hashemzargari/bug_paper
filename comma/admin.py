from django.contrib import admin
from comma.models import Post, Category


@admin.register(Post, Category)
class PostAdmin(admin.ModelAdmin):
    pass
