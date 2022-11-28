from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at', 'get_html_photo', 'is_published', 'category', 'content') #настраивающий класс модели - подкласс admin.ModelAdmin, для того, чтобы регулировать отображение в админке
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',) #указание на то, какие поля редактируются прямо из списка в админке
    list_filter = ('is_published', 'category') #указание, по каким полям хочу фильтровать в админке
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'category', 'content', 'photo', 'get_html_photo', 'is_published', 'created_at', 'updated_at') #порядок и список редактируемых полей, отображаемых в форме редактирования админки
    readonly_fields = ('created_at', 'updated_at', 'get_html_photo') #то же самое, что выше, только для нередактируемых полей
    save_on_top = True #атрибут, позволяющий добавить в админку сверху доп. панель для сохранения объектов

    def get_html_photo(self, object): #object ссылается на объект модели News (текущую запись списка)
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>") #mark_safe позволяет отключить экранирование тэгов, дабы они выполнялись (добавляется фильтр safe)

    get_html_photo.short_description = "Миниатюра"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(News, NewsAdmin) #регистрация модели и настраивающего класса модели (порядок важен! Сначала сама модель, потом настраивающий её класс)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель тестового новостного сайта'
admin.site.site_header = 'Админ-панель тестового новостного сайта 2'
