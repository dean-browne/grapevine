from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

from .models import Post, Comment
from .forms import PostForm, CommentForm

"""
View for: The homepage
"""
def index(request):
    if(request.user.is_authenticated()):
        print "[+] User is authenticated"
        post_list = Post.objects.order_by('-date')
        return render(request, 'home/index.html', {'post_list': post_list})
    else:
        print "[+] User is not authenticated"
        return render(request, 'home/index_unregistered.html')


"""
View for Adding a new post
Requires Login
"""
@login_required
def newPost(request):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        print "[+] (Post) Post request has been received"
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return HttpResponseRedirect(reverse('home:detail', args=(post.id,)))

    else:
        print("[-] (Post) Get request received")
        post_form = PostForm()
        return render(request, 'home/new_post.html', {'post_form': post_form})


"""
View for: The requested posts details (Displays the post and the posts comments)
"""
@login_required
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comment_form = CommentForm
    return render(request, 'home/detail.html', {'post': post, 'comment_form': comment_form})


"""
View for: adding a comment
"""
@login_required
def addComment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        print "[+] Receievd a post request on addComment"

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('home:detail', args=(post.id,)))

    else:
        return render(request, 'home/detail.html', {'post':post, 'comment_form':comment_form})
