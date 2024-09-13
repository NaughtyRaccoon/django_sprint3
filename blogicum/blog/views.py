from django.shortcuts import render, get_object_or_404

from blog.models import Category
from .utils import posts_filter

POSTS_LIMIT = 5


def index(request):
    post_list = posts_filter().order_by('-pub_date')[:POSTS_LIMIT]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        posts_filter(include_author_location=True),
        category__is_published=True,
        pk=post_id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = posts_filter(category=category, include_author_location=True)
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
