from django.contrib import admin
from comma.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
