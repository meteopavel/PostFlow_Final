from django.db.models import Count, Prefetch
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Comment, Location, Post


def get_base_query():
    published_categories = Location.objects.filter(is_published=True)
    return Post.objects.prefetch_related(
        'author',
        'category',
        Prefetch('location', published_categories)
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments')
    ).order_by(
        '-pub_date', 'title'
    )


def get_comment_instance(request, post_pk, comment_pk):
    instance = get_object_or_404(
        Comment,
        pk=comment_pk,
        post_id=post_pk,
    )
    return instance


def get_page_obj(request, post_list):
    paginator = Paginator(post_list, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
