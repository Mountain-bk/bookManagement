from django import forms
from .models import Author, Category, Book
from django.forms.widgets import CheckboxSelectMultiple
from django.core.exceptions import ValidationError


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'published_date',
            'categories',
            'authors'
        ]

        widgets = {
            'published_date': forms.DateInput(attrs={"type": "date"}),
            'categories': CheckboxSelectMultiple(),
            'authors': CheckboxSelectMultiple()
        }

        labels = {
            'title': 'Title',
            'published_date': 'Published Date',
            'categories': 'Category',
            'authors': 'Author'
        }

    def clean(self):
        title = self.cleaned_data.get('title')
        authors = self.cleaned_data.get('authors')
        for author in authors:
            if Book.objects.filter(title=title, authors=author).exclude(id=self.instance.id):
                raise ValidationError("Error")
