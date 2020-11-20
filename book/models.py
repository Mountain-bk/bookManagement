from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    published_date = models.DateField(auto_now=False)
    categories = models.ManyToManyField(Category)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return self.title