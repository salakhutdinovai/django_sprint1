from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, PostForm, CommentForm, UserProfileForm
from .models import Post, Category


def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'index.html', {'posts': posts})


@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', id=id)
    else:
        form = CommentForm()
    return render(request, 'detail.html', {'post': post, 'form': form})


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-pub_date')
    return render(request, 'category.html', {'category': category, 'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:user_profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    return render(request, 'user_profile.html', {'profile_user': user, 'posts': posts})


def search(request):
    category_query = request.GET.get('category', '')
    if category_query:
        posts = Post.objects.filter(category__name__icontains=category_query).order_by('-pub_date')
    else:
        posts = Post.objects.all().order_by('-pub_date')
    return render(request, 'search.html', {'posts': posts, 'query': category_query})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
