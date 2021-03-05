from django.urls import path
from .views import (
	PostListView,
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
	UserPostListView
)
from . import views


urlpatterns = [
	path('', PostListView.as_view(), name='blog-home'),
	path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
	###################  DETAIL POST ################################
	path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
	###################  CREATE POST ################################ 
	path('post/new', PostCreateView.as_view(), name='post-create'),
	###################  UPDATE POST ################################ 
	path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
	###################  DELETE POST ################################ 
	path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
	path('about', views.about, name='blog-about'),
	path('latest', views.latest, name='blog-latest'),
	# path('<str:slug>', views.comment_new, name='blog-comment'),
]