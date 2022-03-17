from django.urls import path
from .views import PostsList, PostDetailView, NewsList, NewsDetail, PostUpdateView, PostDeleteView, PostCreateView

urlpatterns = [
    path('posts/', PostsList.as_view()),
    path('news/', NewsList.as_view()),

    path('search/', PostsList.as_view()),
    path('news/<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('news/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('news/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('news/add/', PostCreateView.as_view(), name='post_create')
]
