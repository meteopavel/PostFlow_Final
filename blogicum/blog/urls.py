from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/<int:pk>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
    path('profile/',
         views.user_edit, name='edit_profile'),
    path('profile/<slug:post_author>/',
         views.user_detail, name='profile'),
    path('posts/<int:pk>/comment/',
         views.add_comment, name='add_comment'),
    path('posts/<int:post_pk>/edit_comment/<int:comment_pk>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_pk>/delete_comment/<int:comment_pk>/',
         views.delete_comment, name='delete_comment'),
]
