from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length = 100)
    published_date = models.DateField(auto_now = False)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

