import pytest
from django.urls import reverse
from book.models import Book, Author, Category
from book.forms import BookForm, AuthorForm, CategoryForm


@pytest.fixture()
def setup_book():
    Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])
    Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])
    b1 = Book(title='星の王子様',
              published_date='2006-03-28')
    b1.save()
    b2 = Book(title='人間の大地', published_date='2015-08-20')
    b2.save()
    c1 = Category.objects.get(name='Novel')
    # c2 = Category.objects.get(name='Design')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤夏樹')
    b1.categories.add(c1)
    b1.authors.add(a1, a2)
    b2.categories.add(c1)
    b2.authors.add(a1)


def test_book_register_case1(setup_book, client):
    c1_pk = Category.objects.get(name='Novel').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk

    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk]
    }
    response = client.post('/book-register/', form_data, follow=True)
    books = list(response.context['books'])
    book_list = []
    for book in books:
        book_list.append(book.title)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Form submission successful'
    assert book_list.count('星の王子様') == 2


def test_book_register_case2(setup_book, client):
    c1_pk = Category.objects.get(name='Novel').pk
    c2_pk = Category.objects.get(name='Design').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    a2_pk = Author.objects.get(name='池澤夏樹').pk

    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk, c2_pk],
        'authors': [a1_pk, a2_pk]
    }
    response = client.post('/book-register/', form_data, follow=True)
    books = list(response.context['books'])
    book_list = []
    for book in books:
        book_list.append(book.title)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, there is an error.'
    assert book_list.count('星の王子様') == 1


def test_book_edit_case1(setup_book, client):
    b1_pk = Book.objects.get(title='人間の大地').pk
    c1_pk = Category.objects.get(name='Novel').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk]
    }
    response = client.post(reverse('book:book edit', kwargs={
                           'id': b1_pk}), form_data, follow=True)

    books = list(response.context['books'])
    book_list = []
    for book in books:
        book_list.append(book.title)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Update submission succesfull'
    assert book_list.count('星の王子様') == 2


def test_book_edit_case2(setup_book, client):
    b1_pk = Book.objects.get(title='人間の大地').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    a2_pk = Author.objects.get(name='池澤夏樹').pk
    c1_pk = Category.objects.get(name='Novel')
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk, a2_pk]
    }
    response = client.post(reverse('book:book edit', kwargs={
                           'id': b1_pk}), form_data, follow=True)
    books = list(response.context['books'])
    book_list = []
    for book in books:
        book_list.append(book.title)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, there is an error.'
    assert book_list.count('星の王子様') == 1
