from django import forms
from .models import Author, Category


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
