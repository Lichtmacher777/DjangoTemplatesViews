from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import User,Post
# Create your views here.
def home(request):
    return render(request,'social_app/homepage.html')


def user_list(request):
    users = User.objects.all()
    return render(request,'social_app/user_list.html',{'users':users})

def user_details(request,username):
    user = get_object_or_404(User,username=username)
    return render(request,'social_app/user_detail.html',{'user':user})

def post_list(request):
    posts = Post.objects.all()
    return render(request,'social_app/post_list.html',{'posts':posts})

def post_detail(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'social_app/post_detail.html', {'post': post})
    
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    return render(request, 'social_app/user_posts.html', {'user': user, 'posts': posts})