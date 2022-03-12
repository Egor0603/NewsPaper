from django.views.generic import ListView, DetailView
from .models import Post
from .filters import PostFilter
from django.core.paginator import Paginator


class PostsList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-created')
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


class NewsDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'



