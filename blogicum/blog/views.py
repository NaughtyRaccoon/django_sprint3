from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from blog.models import Post, Category


def index(request):
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).select_related('author', 'location', 'category'),
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
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).select_related('author', 'location', 'category')
    context = {
        'category': category,
        'post_list': posts,
    }
    return render(request, 'blog/category.html', context)
