from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from .signals import check_post_today

from django.core.paginator import Paginator


class PostsList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-created')
    paginate_by = 1

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            'filter': self.get_filter()
        }


class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        cats_id_list = list(map(int, request.POST.getlist('category')))
        category = Category.objects.filter(pk__in=cats_id_list)
        new_post = Post(title=request.POST['title'],
                        text=request.POST['text'],
                        author=Author.objects.get(pk=request.POST['author']),
                        # type=request.POST['post_type']
                        )
        if check_post_today(sender=Post, instance=new_post, **kwargs) < 3:
            new_post.save()
            for cat in category:
                new_post.category.add(cat)

        return redirect('/news/search/')


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'post_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/search/'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


def subscribe(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    for category in post.cats.all():
        user = User.objects.get(pk=request.user.id)
        category.subscribers.add(user)
    return redirect('/news/search')
