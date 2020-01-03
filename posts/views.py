from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

def get_posts(request):
    """Create a view that will return 
    a list of posts published prior to 'now'
    and render them to blogposts.html"""

    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, "blogposts.html", {"posts":posts})

def post_detail(request, pk):
    """Create a view that returns 
    a single post object based on post ID(pk)
    and render to postdetail.html template
    or return error 404 if not found"""

    post = get_object_or_404(Post, pk=pk)
    post.views +=1
    post.save()
    return render(request, "postdetail.html", {"post":post})

def create_or_edit_a_post(request, pk=None):
    """Create a view that allows us to create or edit a post
    depending if the post ID(pk) is null or not"""

    post = get_object_or_404(Post, pk=pk) if pk else None

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post_detail, post.pk)
    else: 
        form = BlogPostForm(instance=post)
    return render(request, "blogpostform.html", {"form": form})


