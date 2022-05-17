from django.urls import path
from .views import PostsList, PostDetailView, NewsList, PostUpdateView, PostDeleteView, PostCreateView, IndexView, \
    subscribe

urlpatterns = [
    path('posts/', PostsList.as_view()),
    path('news/', NewsList.as_view()),

    path('search/', PostsList.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),

    path('index/', IndexView.as_view(), name='index'),

    path('subscribe/<int:pk>', subscribe, name='subscribe'),
]
