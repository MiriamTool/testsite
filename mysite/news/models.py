from django.db import models
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def my_func(self):
        return 'Hello from model'

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_slug": self.slug}) #здесь раньше был news_id, но теперь тут слаг



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['created_at']

class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=150, unique=True, db_index=True,
                           verbose_name='URL')

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_slug": self.slug}) #kwargs - именованные аргументы для построения данного маршрута. Метод нужен для автосоздания ссылки, аналог тега url для пайтон-файлов

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']