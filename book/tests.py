from django.test import TestCase
import pytest
from .models import Book, Author, Category
from .forms import BookForm, AuthorForm, CategoryForm

# Create your tests here.


@pytest.fixture(autouse=True)
@pytest.mark.django_db
def setup():
    c1 = Category(name='Novel')
    c1.save()
    a1 = Author(name='サン・テグジュペリ')
    a1.save()
    b1 = Book(title='星の王子様',
              published_date='2006-03-28')
    b1.save()
    b1.categories.add(c1)
    b1.authors.add(a1)


@pytest.mark.django_db
def test_duplicate_book_register_form():
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    b2 = BookForm(
        {
            'title': '星の王子様',
            'published_date': '2006-03-28',
            'categories': [c1],
            'authors': [a1]
        }
    )
    if b2.is_valid():
        b2.save()
    else:
        pass
    # count will be 1 if it's duplicate register
    assert Book.objects.count() == 1
