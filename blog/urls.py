from django.urls import path
from .views import PostListView, PostCreateView, search
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.view_post, name='post-detail'),
    path('search/', search, name='search'),
]
