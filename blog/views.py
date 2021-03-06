from django.shortcuts import render
from django.utils import timezone
from .models import blogPost
from .forms import PostForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = blogPost.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(blogPost, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


