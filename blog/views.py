from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import PostUserForm
from .models import *
from django.db.models import F


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все новости'
        return context


class PostsByCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'blog/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s-{self.request.GET.get('s')}&"
        return context


def add_post(request):
    if request.method == "POST":
        post_form = PostUserForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
            return redirect(post.get_absolute_url())
    else:
        post_form = PostUserForm()
    return render(request, 'add-post.html', locals())


def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post_form = PostUserForm(request.POST or None, instance=post)
    if post_form.is_valid():
        post = post_form.save()
    return render(request, 'update-post.html', locals())


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Пост удален.')
        return redirect('home')
    return render(request, 'delete-recipe.html')
