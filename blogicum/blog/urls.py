from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path('<int:post_pk>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_pk>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('<int:post_pk>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('<int:post_pk>/comment/',
         views.add_comment, name='add_comment'),
    path('<int:post_pk>/edit_comment/<int:comment_pk>/',
         views.edit_comment, name='edit_comment'),
    path('<int:post_pk>/delete_comment/<int:comment_pk>/',
         views.delete_comment, name='delete_comment'),
]

profile_urls = [
    path('',
         views.user_edit, name='edit_profile'),
    path('<str:post_author>/',
         views.user_detail, name='profile'),
]

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path('profile/', include(profile_urls)),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]
