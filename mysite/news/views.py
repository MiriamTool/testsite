from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm

from .models import News, Category
from .forms import *
from .utils import *

class HomeNews(ListView):
    paginate_by = 3
    model = News #модель, из которой получается список, аналог news = News.objects.all()
    template_name = 'news/home_news_list.html' #жесткое задание шаблона, иначе назначится дефолтное имя news_list.html
    context_object_name = 'news' #переименование контекстного объекта, по дефролту был бы object_list
    # extra_context = {'title': 'Главная'} не рекомендуется использовать, лучше использовать как ниже метод гет_контекст_дата, возвращающую модифицированный контекст

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category') #фильтр запроса для query_set, передаём только новости, у которых is_published == 1
    # Select_related - жадный запрос для оптимизации вывода категорий статей в файле home_news_list.html

class NewsByCategory(DataMixin, ListView): #DataMixin - класс, от которого наследуется метод get_user_context
    paginate_by = 3
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    slug_url_kwarg = 'category_slug'
    allow_empty = False #запрещает обращаться к пустому списку, т.е. блокирует выведение категорий, в которых нет опубликованных новостей, либо несуществующих категорий

    # def get_queryset(self):
    #     return News.objects.filter(category_id=self.kwargs['category_id'],
    #                                is_published=True)

    def get_queryset(self):
        return News.objects.filter(category__slug=self.kwargs['category_slug'],
                                   is_published=True).select_related('category') #оптимизация с помощью жадных запросов


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
    #     return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        context = dict(list(context.items()) + list(c_def.items()))
        # context['title'] = Category.objects.get(slug=self.kwargs['category_slug']) #убираем, т.к. в классе DataMixin прописана эта строчка

        return context


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    slug_url_kwarg = 'news_slug'
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html' #дефолтное значение имени темплейта *_detail

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = reverse_lazy('home')
    raise_exception = True # Выводит ошибку 403 - доступ запрещён

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Добавить новость'
    #     return context
    # success_url = reverse_lazy('home') #по дефолту при успешном выполнении, редирект происходит на ссылку, которая автоматически получается методом get_absolute_url модели, но можно прописать свой путь


# def index(request):
#     print(request)
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context=context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id) #применение функции для получения объекта либо вывода 404 ошибки вместо 500 ошибки (ошибка сервера)
#     return render(request, 'news/view_news.html', {'news_item': news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST, error_class=DivErrorList)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data) #Две звезды - автораспаковка словаря в питоне, cleaned_data - готовый к упротреблению словарик отвалидированных данных
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Страница регистрации'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')