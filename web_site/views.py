from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Category, Post, Comments
# Create your views here.
from .forms import PostForm, LoginForm, UserRegister, AddComment
from django.contrib.auth import login, logout
from django.views.generic import DetailView, DeleteView, UpdateView, ListView, CreateView
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q


class Index(ListView):
    model = Post
    template_name = 'web_site/index.html'
    extra_context = {
        'title': 'Главная страница2'
    }
    context_object_name = 'posts'


class ShowByCategory(Index):
    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        Context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        Context['title'] = category.title
        return Context


class ArticleDetail(DetailView):
    model = Post
    template_name = 'web_site/article_detail.html'

    def get_queryset(self):
        return Post.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Post.objects.get(pk=self.kwargs['pk'])
        articles = Post.objects.all()
        posts = articles.order_by('-watched')[:4]

        article.watched += 1
        article.save()
        context['title'] = article.title
        context['comments'] = Comments.objects.filter(post=article)
        context['posts'] = posts

        if self.request.user.is_authenticated:
            context['comment_form'] = AddComment()

        return context


class AddPost(CreateView):
    form_class = PostForm
    template_name = 'web_site/article_form.html'
    extra_context = {
        'title': 'Добавить статью'
    }

    def get_queryset(self):
        return Post.objects.filter()


class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'web_site/article_form.html'


class ArticleDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('index')
    context_object_name = 'post'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')

    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }

    return render(request, 'web_site/login_form.html', context)


# TODO Отлов ошибки
# Сообщения

def user_logout(request):
    logout(request)
    return redirect('index')


def user_register(request):
    if request.method == 'POST':
        form = UserRegister(data=request.POST)
        if form.is_valid():
            User = form.save()
            return redirect('login')
    else:
        form = UserRegister()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'web_site/register_form.html', context)


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    articles = Post.objects.filter(author=user)
    context = {
        'user': user,
        'title': 'Страница пользователя',
        'articles': articles
    }
    return render(request, 'web_site/profile.html', context)


class Search(Index):
    def get_queryset(self):
        word = self.request.GET.get('q')
        articles = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return articles



def add_comment(request, article_id):
    form = AddComment(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        post = Post.objects.get(pk=article_id)
        comment.post = post
        comment.save()
        messages.success(request, 'Ваш комментарий успешно добавлен')
    else:
        pass

    return redirect('post_detail', article_id)
