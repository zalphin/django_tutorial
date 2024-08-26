# posts/urls.py
from django.urls import path

from .views import PostListView, PostDetailView

app_name = 'posts'
urlpatterns = [
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('', PostListView.as_view(), name="post_list"),
]