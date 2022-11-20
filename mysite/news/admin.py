from django.contrib import admin

from .models import News, Category

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'is_published', 'category') #настраивающий класс модели - подкласс admin.ModelAdmin, для того, чтобы регулировать отображение в админке
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',) #указание на то, какие поля редактируются прямо из списка в админке
    list_filter = ('is_published', 'category') #указание, по каким полям хочу фильтровать в админке
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(News, NewsAdmin) #регистрация модели и настраивающего класса модели (порядок важен! Сначала сама модель, потом настраивающий её класс)
admin.site.register(Category, CategoryAdmin)
