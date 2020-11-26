from django import forms
from .models import Author, Category


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
