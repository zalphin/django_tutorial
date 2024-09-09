from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = "post_list.html"
    title = "Blog index"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"
    title = "Post details"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context