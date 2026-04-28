from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required(login_url='/oauth/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('ion_login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required(login_url='/oauth/login/')
def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You can only edit your own posts.")
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required(login_url='/oauth/login/')
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden("You can only delete your own posts.")
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})