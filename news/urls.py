from django.urls import path
from .views import PostsList, PostDetail, NewsList, NewsDetail

urlpatterns = [
    path('posts/', PostsList.as_view()),
    path('posts/<int:pk>', PostDetail.as_view()),
    path('news/', NewsList.as_view()),
    path('news/<int:pk>', NewsDetail.as_view()),
    path('news/search/', PostsList.as_view()),

]
