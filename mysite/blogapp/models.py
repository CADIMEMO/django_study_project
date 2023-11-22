from django.db import models
from django.db.models import Model
# Create your models here.


class Author(Model):
    name = models.CharField(max_length=100, null=False)
    bio = models.TextField(blank=True)


class Category(Model):
    name = models.CharField(max_length=30, null=False)


class Tag(Model):
    name = models.CharField(max_length=20, null=False)


class Article(Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='articles')