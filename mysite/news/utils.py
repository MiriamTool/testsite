from .models import *
from django.core.cache import cache

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        #context['title'] = cache.get('title')
        #if not context['title']:
        context['title'] = Category.objects.get(
                slug=self.kwargs['category_slug'])
        #    cache.set('title', context['title'], 60) #весь этот кэш работает, но не слишком хорошо, т.к. у меня категория везде из кэша берётся, а значит при загрузке страницы с этим Миксином (новости по категориям), у меня будет в тайтл выводить название группы новостей из кэша при нажатии на любую категорию
        return context