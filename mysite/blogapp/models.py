from django.db import models
from django.db.models import Model
from django.urls import reverse


# Create your models here.


class Author(Model):
    name = models.CharField(max_length=100, null=False)
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Category(Model):
    name = models.CharField(max_length=30, null=False)
    def __str__(self):
        return self.name


class Tag(Model):
    name = models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.name


class Article(Model):
    title = models.CharField(max_length=200, null=False)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='articles')

    def get_absolute_url(self):
        return reverse('blogapp:article_details', kwargs={'pk': self.pk})
