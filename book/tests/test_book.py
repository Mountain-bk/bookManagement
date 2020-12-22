import pytest
from django.urls import reverse
from book.models import Book, Author, Category
from book.forms import BookForm, AuthorForm, CategoryForm


@pytest.fixture()
def setup_book_objects():
    # Create Category('Novel' and 'Deisgn')
    Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])
    # Create Author('サン・テグジュペリ' and '池澤夏樹')
    Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])
    # get Category and Author
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤夏樹')
    # Create Book(1)
    b1 = Book(title='星の王子様',
              published_date='2006-03-28')
    b1.save()
    b1.categories.add(c1)
    b1.authors.add(a1, a2)
    # Create Book(2)
    b2 = Book(title='人間の大地', published_date='2015-08-20')
    b2.save()
    b2.categories.add(c1)
    b2.authors.add(a1)


def test_book_register_with_same_title(setup_book, client):
    """Book will be registred if same title exists but authors don't match"""
    c1_pk = Category.objects.get(name='Novel').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    # create form data for POST
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk]
    }
    # POST from book register page
    response = client.post('/book-register/', form_data, follow=True)
    # retrieve 'book' context from response
    books = list(response.context['books'])
    # create list of books from response(all books in db)
    book_list = []
    for book in books:
        book_list.append(book.title)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Success message
    assert response_message.message == 'Form submission successful'
    # 2 books exists with same title
    assert book_list.count('星の王子様') == 2


def test_book_register_with_same_title_and_author(setup_book, client):
    """Book won't be registred if same title exists and authors match"""
    c1_pk = Category.objects.get(name='Novel').pk
    c2_pk = Category.objects.get(name='Design').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    a2_pk = Author.objects.get(name='池澤夏樹').pk
    # create form data for POST
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk, c2_pk],
        'authors': [a1_pk, a2_pk]
    }
    # POST from book register page
    response = client.post('/book-register/', form_data, follow=True)
    # retrieve 'book' context from response
    books = list(response.context['books'])
    # create list of books from response(all books in db)
    book_list = []
    for book in books:
        book_list.append(book.title)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Error message
    assert response_message.message == 'Sorry, there is an error.'
    # 1 book exists, not 2
    assert book_list.count('星の王子様') == 1


def test_book_edit_with_same_title(setup_book, client):
    """Book will be updated if same title exists but authors don't match"""
    b1_pk = Book.objects.get(title='人間の大地').pk
    c1_pk = Category.objects.get(name='Novel').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    # create form data for POST
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk]
    }
    # POST from book register page
    response = client.post(reverse('book:book edit', kwargs={
                           'id': b1_pk}), form_data, follow=True)
    # retrieve 'book' context from response
    books = list(response.context['books'])
    # create list of books from response(all books in db)
    book_list = []
    for book in books:
        book_list.append(book.title)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Success message
    assert response_message.message == 'Update submission succesfull'
    # 2 books exists with same title
    assert book_list.count('星の王子様') == 2


def test_book_edit_with_same_title_and_author(setup_book, client):
    """Book won't be updated if same title exists and authors match"""
    b1_pk = Book.objects.get(title='人間の大地').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    a2_pk = Author.objects.get(name='池澤夏樹').pk
    c1_pk = Category.objects.get(name='Novel').pk
    # create form data for POST
    form_data = {
        'title': '星の王子様',
        'published_date': '2015-08-20',
        'categories': [c1_pk],
        'authors': [a1_pk, a2_pk]
    }
    # POST from book register page
    response = client.post(reverse('book:book edit', kwargs={
                           'id': b1_pk}), form_data, follow=True)
    # retrieve 'book' context from response
    books = list(response.context['books'])
    # create list of books from response(all books in db)
    book_list = []
    for book in books:
        book_list.append(book.title)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Error message
    assert response_message.message == 'Sorry, there is an error.'
    # 1 book exists, not 2
    assert book_list.count('星の王子様') == 1
