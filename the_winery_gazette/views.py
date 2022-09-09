from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm, PostArticleForm


def the_gazette(request):
    """ A view to render the Gazette's articles on the page """

    posts = Post.objects.filter(status=1).all()
    template_name = 'the_winery_gazette/the_gazette.html'

    context = {
        'posts': posts,
    }

    return render(request, template_name, context)


def post_detail(request, slug):
    """ A view to render a specific Gazette article in detail """

    template_name = 'the_winery_gazette/gazette_post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'form': form,
    }

    return render(request, template_name, context)


def add_post(request):
    """ Add a new post to the Winery Gazette """
    if request.method == "POST":
        form = PostArticleForm(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.title = request.POST["title"]
            new_post.slug = request.POST["slug"]
            new_post.image = request.POST["image"]
            new_post.content = request.POST["content"]
            new_post.status = request.POST["status"]
            new_post.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            form = PostArticleForm()
            context = {
                'form': form
            }
        return render(request,'the_winery_gazette/add_post.html', context)
    else:
        return redirect('home')
