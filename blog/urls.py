from django.urls import path

from .views import *


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('addpost/', add_post, name='add-post'),
    path('update-post/<str:slug>/', update_post, name='update-post'),
    path('delete-post/<str:slug>/', delete_post, name='delete-post'),
]