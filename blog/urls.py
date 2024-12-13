from django.urls import path
from blog.views import post_list, post_detail, post_share, post_search
from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name = 'post_list'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name = 'post_detail'),
    path('<int:post_id>/share/', post_share, name = 'post_share'),
    path('feed/', LatestPostFeed(), name = 'post_feed'),
    path('search/', post_search, name='post_search')
]