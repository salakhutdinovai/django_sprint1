from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
    path('register/', views.register, name='register'),
    path('create/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.user_profile, name='user_profile'),
]