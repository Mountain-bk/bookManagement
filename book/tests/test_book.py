import pytest
from django.urls import reverse
from book.models import Book, Author, Category


@pytest.fixture()
def setup_book_objects():
    Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])
    Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤夏樹')
    b1 = Book(title='星の王子様',
              published_date='2006-03-28')
    b1.save()
    b1.categories.add(c1)
    b1.authors.add(a1, a2)
    b2 = Book(title='人間の大地', published_date='2015-08-20')
    b2.save()
    b2.categories.add(c1)
    b2.authors.add(a1)


# 同じタイトルでも著者が一致していなければ登録が出来ることをテスト
def test_book_register_with_same_title(setup_book_objects, client):
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
    expected_list = ['星の王子様', '星の王子様', '人間の大地']
    assert sorted(expected_list) == sorted(book_list)


# 「同じタイトルかつ同じ著者」の組み合わせの本が存在する場合は登録が拒否されることをテスト
def test_book_register_with_same_title_and_author(setup_book_objects, client):
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
    expected_list = ['星の王子様', '人間の大地']
    assert sorted(expected_list) == sorted(book_list)


# 同じタイトルでも著者が一致してなければ編集が出来ることをテスト
def test_book_edit_with_same_title(setup_book_objects, client):
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
    expected_list = ['星の王子様', '星の王子様']
    assert sorted(expected_list) == sorted(book_list)


# 「同じタイトルかつ同じ著者」の組み合わせの本が存在する場合は編集が拒否されることをテスト
def test_book_edit_with_same_title_and_author(setup_book_objects, client):
    b1_pk = Book.objects.get(title='人間の大地').pk
    a1_pk = Author.objects.get(name='サン・テグジュペリ').pk
    a2_pk = Author.objects.get(name='池澤夏樹').pk
    c1_pk = Category.objects.get(name='Novel').pk
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
    expected_list = ['星の王子様', '人間の大地']
    assert sorted(expected_list) == sorted(book_list)
