from django.contrib import admin
from django.contrib.admin import register

from blog.models import Post


@register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'publish']