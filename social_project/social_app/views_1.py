from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView,UpdateView,CreateView,DeleteView
from django.http import HttpResponse
from .models import User, Post
from django.urls import reverse_lazy
from .form_1 import UserForm,PostForm
from django.contrib.auth.views import LoginView, LogoutView
from .form_1 import LoginForm
import logging
logger = logging.getLogger(__name__)

class HomePageView(TemplateView):
    template_name = 'social_app/homepage.html'


class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name ='social_app/user_list.html'
    
class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'social_app/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'social_app/post_list.html'
    

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'social_app/post_detail.html'
    pk_url_kwarg = 'post_id'
    
    
class UserPostsView(ListView):
    model = Post
    template_name = 'social_app/user_posts.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        print(context)
        print('*'*100)
        username = self.kwargs['username']
        user = get_object_or_404(User,username = username)
        context['user']= user
        print(context)
        return context
    
    def get_queryset(self) :
        username = self.kwargs['username']
        user = get_object_or_404(User , username = username)
        return Post.objects.filter(user=user).order_by('-created_at')
    
    
class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name ='social_app/user_form.html'
    success_url = reverse_lazy('user_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f'User created {self.object.username}')
        return response
            
class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social_app/post_form.html'
    def form_valid(self,form):
        user = get_object_or_404(User,username=self.kwargs['username'])
        form.instance.user = user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_detail',kwargs ={'username':self.object.user.username})
    
    
class UpdateUserView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'social_app/user_form.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(User,username = self.kwargs['username'])
    def get_success_url(self):
        return reverse_lazy('user_detail', kwargs={'username': self.object.username})
    def form_valid(self, form):
        response = super().form_valid(form)
        logger.debug(self.request)
        logger.info(f"User updated: {self.object.username}")
        return response
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        logger.warning(f"User update failed: {self.object.username}")
        return response
   
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'social_app/post_form.html'
    form_class = PostForm
    pk_url_kwarg ='post_id'
    slug_url_kwarg = 'username'
    slug_field ='username'
    def get_success_url(self):
        return reverse_lazy('user_posts', kwargs={'username': self.object.user.username})
    def get_object(self, queryset=None):
        return get_object_or_404(Post,id = self.kwargs['post_id'])

 
class DeleteUserView(DeleteView):
    model = User
    template_name = 'social_app/delete_user.html'
    success_url =reverse_lazy('user_list')
    slug_url_kwarg = 'username'
    slug_field ='username'
    
class DeletePostView(DeleteView):
    model = Post
    template_name = 'social_app/delete_post.html'
    pk_url_kwarg ='post_id'
    slug_url_kwarg = 'username'
    slug_field ='username'
    def get_success_url(self):
        return reverse_lazy('user_posts', kwargs={'username': self.object.user.username})
 
    
class MyLoginView(LoginView):
    form_class = LoginForm
    template_name = 'social_app/login.html'

class MyLogoutView(LogoutView):
    # You can customize this view if needed
    template_name = 'social_app/logout.html'