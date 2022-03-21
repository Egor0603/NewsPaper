from django.urls import path
from .views import PostsList, PostDetailView, NewsList, PostUpdateView, PostDeleteView, PostCreateView, IndexView

urlpatterns = [
    path('posts/', PostsList.as_view()),
    path('news/', NewsList.as_view()),

    path('search/', PostsList.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),

    # path('', IndexView.as_view())
]
