from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/", views.posts_overview, name="posts_overview"),
    path("tags/", views.tags_overview, name="tags_overview"),
    path("posts/<int:id>/", views.post, name="post"),
    path("tags/<int:id>/", views.posts_filtered_by_tag, name="posts_by_tag"),
    path("rss/", views.RssFeed(), name="rss"),
]
