from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-имя категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    display_name = models.CharField(max_length=150, verbose_name="Отображаемое имя")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Уникальный адрес страницы")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")

    def __str__(self):
        return f"{self.display_name} ({self.user.username})"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст поста")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    location = models.CharField(max_length=200, blank=True, verbose_name="Локация")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_moderated = models.BooleanField(default=False, verbose_name="Проверено модератором")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="Пост")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_moderated = models.BooleanField(default=False, verbose_name="Проверено модератором")

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.post.title}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['created_at']
