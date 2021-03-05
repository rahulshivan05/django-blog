from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib.auth.models	import User
from django.core.paginator import Paginator
from django.views.generic import (
									ListView,
									DetailView,
									CreateView,
									UpdateView,
									DeleteView
								)
from .models import Post
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from hitcount.views import HitCountDetailView
import requests
from django_user_agents.utils import get_user_agent

# print(dir(requests))
import user_agents

def home(request):
	print(request.user_agent.is_mobile)
	context = {
		'posts': Post.objects.all(),
		'today': now().date()
	}
	return render(request, 'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_post.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(HitCountDetailView):
	model = Post
	count_hit = True
	# print("get_current_site: ", get_current_site(request))


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	success_message = 'Post successful created'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False		


def about(request):
	print(request.user_agent.is_pc)
	print(request.user_agent.browser)
	print(request.user_agent.os)
	return render(request, 'blog/about.html', {'title': 'About'})

def latest(request):
	allPosts = Post.objects.order_by('-date_posted')[:5]
	return render(request, 'blog/latest.html', {'allPosts': allPosts})


# def comment_new(request):
#     if request.method == 'POST':
#         message = request.POST['comment']
#         subject = request.POST['title']
#         user = request.user
#         # lastname = request.POST['lastname']

#         send_mail("[MAIL] " + subject, user + " " +" said  " + message + " on http://127.0.0.1:8000/"+url,
#                   'guillermo.varelli@gmail.com',
#                   ['guillermo.varelli@gmail.com'], fail_silently=False)
#     posts = Post.objects.all().order_by('-created')
#     content = {
#     	'posts': posts,
#     }
#     return redirect(f'')


