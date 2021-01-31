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
        try:
            title = self.cleaned_data.get('title')
            authors = self.cleaned_data.get('authors')
            authors = list(authors.values_list('name', flat=True))
            same_books = list(Book.objects.filter(
                title=title).exclude(id=self.instance.id))  # タイトルが同じ本のリストを作成
            for same_book in same_books:  # タイトルが同じ本の著者を順に調べる
                exist_authors = list(
                    same_book.authors.values_list('name', flat=True))  # 存在する著者のリストを作成
                if exist_authors == authors:  # 送信した著者と存在する著者が一致した場合エラー
                    raise ValidationError("Error")
        except:
            raise ValidationError("Error")
