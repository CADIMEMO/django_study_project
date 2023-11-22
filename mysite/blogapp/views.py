from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from .models import Article, Author, Tag, Category
from django.urls import reverse_lazy, reverse
from .forms import ArticleForm
# Create your views here.


class BaseView(TemplateView):
    template_name = 'blogapp/base.html'


class ArticleList(ListView):
    model = Article
    queryset = Article.objects.all()
    context_object_name = 'articles'
    template_name = 'blogapp/article_list.html'


class CreateArticle(CreateView):
    model = Article
    template_name = 'blogapp/create_article.html'
    # fields = ['title', 'content', 'author', 'category', 'tags']
    form_class = ArticleForm
    success_url = reverse_lazy('blogapp:article_list')


class CreateAuthor(CreateView):
    model = Author
    template_name = 'blogapp/create_author.html'
    fields = ['name', 'bio']
    success_url = reverse_lazy('blogapp:article_list')


class CreateTag(CreateView):
    model = Tag
    template_name = 'blogapp/create_tag.html'
    fields = ['name']
    success_url = reverse_lazy('blogapp:article_list')


class CreateCategory(CreateView):
    model = Category
    template_name = 'blogapp/create_category.html'
    fields = ['name']
    success_url = reverse_lazy('blogapp:article_list')
