from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from .models import News, Category
from .forms import NewsForm, DivErrorList

class HomeNews(ListView):
    model = News #модель, из которой получается список, аналог news = News.objects.all()
    template_name = 'news/home_news_list.html' #жесткое задание шаблона, иначе назначится дефолтное имя news_list.html
    context_object_name = 'news' #переименование контекстного объекта, по дефролту был бы object_list
    # extra_context = {'title': 'Главная'} не рекомендуется использовать, лучше использовать как ниже метод гет_контекст_дата, возвращающую модифицированный контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True) #фильтр запроса для query_set, передаём только новости, у которых is_published == 1

def index(request):
    print(request)
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, 'news/index.html', context=context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

def view_news(request, news_id):
    #news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id) #применение функции для получения объекта либо вывода 404 ошибки вместо 500 ошибки (ошибка сервера)
    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, error_class=DivErrorList)
        if form.is_valid():
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data) #Две звезды - автораспаковка словаря в питоне, cleaned_data - готовый к упротреблению словарик отвалидированных данных
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
