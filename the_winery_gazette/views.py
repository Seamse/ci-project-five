from django.shortcuts import render
from django.views import generic
from .models import Post


def the_gazette(request):
    """ A view to render the Gazette's articles on the page """

    posts = Post.objects.filter(status=1).all()
    template_name = 'the_winery_gazette/the_gazette.html'

    context = {
        'posts': posts
    }

    return render(request, template_name, context)


# class GazettePostDetail(generic.DetailView):
#     """ A view to show the details of a specific post/article """

#     model = Post
#     template_name = 'the_winery_gazette/gazette_post_detail.html'
