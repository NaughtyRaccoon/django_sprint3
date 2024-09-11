from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


SORT_ORDER_BY_PUB_DATE = '-pub_date'


def posts_filter(category=None, include_author_location=False):
    filters = {
        'is_published': True,
        'pub_date__lte': timezone.now(),
        'category__is_published': True
    }
    if category:
        filters['category'] = category

    queryset = Post.objects.filter(**filters)
    if include_author_location:
        queryset = queryset.select_related('author', 'location', 'category')
    else:
        queryset = queryset.select_related('category')

    return queryset


def index(request):
    post_list = posts_filter().order_by(SORT_ORDER_BY_PUB_DATE)[:5]
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
