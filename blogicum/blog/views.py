from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .forms import CommentForm, PostForm, UpdateUserForm
from .models import Category, Comment, Post, User


def get_base_query():
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )


def get_page_obj(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'post_author': self.request.user.username})


class PostEditMixin:

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if instance.author != request.user:
            return redirect('blog:post_detail', instance.pk)
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = get_base_query()
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['pk'])
        if (instance.author != request.user
           and (not instance.is_published
                or not instance.category.is_published
                or not instance.pub_date <= timezone.now())):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comment.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PostMixin, PostEditMixin, UpdateView):
    pass


class PostDeleteView(LoginRequiredMixin, PostMixin, PostEditMixin, DeleteView):
    pass


def category_posts(request, category_slug):
    template_name = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug,
    )
    post_list = get_base_query(
    ).filter(
        category__slug=category_slug
    )
    page_obj = get_page_obj(request, post_list)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template_name, context)


def user_detail(request, post_author):
    template_name = 'blog/profile.html'
    profile = get_object_or_404(User, username=post_author)
    post_list = Post.objects.filter(author__username=post_author)
    page_obj = get_page_obj(request, post_list)
    context = {'profile': profile, 'page_obj': page_obj}
    return render(request, template_name, context)


@login_required
def user_edit(request):
    instance = get_object_or_404(User, pk=request.user.id)
    form = UpdateUserForm(request.POST or None, instance=instance)
    template_name = 'blog/user.html'
    context = {'form': form}
    if form.is_valid():
        form.save()
    return render(request, template_name, context)


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


@login_required
def edit_comment(request, post_pk, comment_pk):
    instance = get_object_or_404(Comment, pk=comment_pk, author=request.user)
    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form, 'comment': instance}
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', pk=post_pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, comment_pk):
    instance = get_object_or_404(Comment, pk=comment_pk, author=request.user)
    context = {'comment': instance}
    if request.method == 'POST':
        instance.delete()
        return redirect('blog:post_detail', pk=post_pk)
    return render(request, 'blog/comment.html', context)
