from django.contrib import admin
from django.urls import path, include
from .views import BaseView, CreateArticle, CreateAuthor, CreateTag, CreateCategory, ArticleList

app_name = 'blogapp'

urlpatterns = [
    path('', BaseView.as_view(), name='blog'),
    path('create_article/', CreateArticle.as_view(), name='create_article'),
    path('create_author/', CreateAuthor.as_view(), name='create_author'),
    path('create_tag/', CreateTag.as_view(), name='create_tag'),
    path('create_category/', CreateCategory.as_view(), name='create_category'),
    path('article_list/', ArticleList.as_view(), name='article_list')


]

