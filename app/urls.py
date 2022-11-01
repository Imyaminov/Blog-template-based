from django.urls import path
from . import views
from . import feeds

urlpatterns = [
    path('home/', views.HomePostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('home/user/<str:username>', views.UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/new_comment', views.CommentCreateView.as_view(), name='comment-create'),
    path('post/category/<str:category_name>', views.CategoryPostListView.as_view(), name='category-post'),
    path('post/<int:pk>/<slug:slug>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/new', views.PostCreateView.as_view(), name='post-create'),
    path('post/feed', feeds.LatestPostsFeed(), name='post-feed'),
]


