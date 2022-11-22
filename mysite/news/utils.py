from .models import *

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = Category.objects.get(
            slug=self.kwargs['category_slug'])
        return context