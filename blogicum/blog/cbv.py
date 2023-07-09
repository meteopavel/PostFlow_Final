"""Страница категории от Зарицкого"""
"""
class CategoryPost(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10
    #allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            ).annotate(comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(
            slug=self.kwargs['category_slug']
        )
        return context
"""
