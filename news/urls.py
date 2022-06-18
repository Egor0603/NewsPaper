from django.urls import path
from .views import PostsList, PostDetailView, NewsList, PostUpdateView, PostDeleteView, PostCreateView, IndexView, \
    subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('posts/', PostsList.as_view()),
    path('news/', NewsList.as_view()),

    path('search/', cache_page(300)(PostsList.as_view())),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),

    path('index/', cache_page(60)(IndexView.as_view()), name='index'),

    path('subscribe/<int:pk>', subscribe, name='subscribe'),
]
