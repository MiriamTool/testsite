from django.urls import path, include
import debug_toolbar

from .views import *

urlpatterns = [
    # path('', index, name='home'),
    path('', HomeNews.as_view(), name='home'),
    # path('category/<int:category_id>/', get_category, name='category'),
    path('category/<slug:category_slug>/', NewsByCategory.as_view(),
         name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    # path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/<slug:news_slug>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news', CreateNews.as_view(), name='add_news'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
]
