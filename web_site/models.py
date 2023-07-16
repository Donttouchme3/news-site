from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')  # Максимум 150 символов

    # id писать не надо. Джанго сделает его сам

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок статьи')  # Заголовок
    content = models.TextField(default='Здесь будет описание статьи. Скоро....',
                               verbose_name='Текст статьи')  # Описание
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')  # Автоматически возьмет дату создания объекта
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')  # Берет дату любого изменения в объекте
    photo = models.ImageField(upload_to='photos/', blank=True, null=True,
                              verbose_name='Изображение')  # blank=True - не обязательна для заполнения
    # null=True - может быть пустой в базе
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано ли')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, default=None, null=True, blank=True, on_delete=models.CASCADE)

    # TODO добавить автора

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

