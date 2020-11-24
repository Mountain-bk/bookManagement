from django import forms
from .models import Book, Category, Author
from django.forms.widgets import CheckboxSelectMultiple


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
