import pytest
from django.urls import reverse
from book.models import Author


@pytest.fixture()
def setup_author_objects():
    # Set up Author('サン・テグジュペリ' and '池澤夏樹')
    return Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])


def test_author_register_with_not_existing_name(setup_author_objects, client):
    """Author will be registred if same name don't exists"""
    # create form data for POST
    form_data = {'name': '村上春樹'}
    # POST from author-register page
    response = client.post('/author-register/', form_data, follow=True)
    # retrieve 'authors' context from response
    authors = list(response.context['authors'])
    # create list of authors from response(all authors in db)
    author_list = []
    for author in authors:
        author_list.append(author.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve success message and author_list matches expected_list if form submission success
    assert response_message.message == 'Form submission successful'
    expected_list = ['サン・テグジュペリ', '池澤夏樹', '村上春樹']
    assert sorted(expected_list) == sorted(author_list)


def test_author_register_with_existing_name(setup_author_objects, client):
    """Author won't be registred if same name exists"""
    # create form data for POST
    form_data = {'name': 'サン・テグジュペリ'}
    # POST from author-register page
    response = client.post('/author-register/', form_data, follow=True)
    # retrieve 'authors' context from response
    authors = list(response.context['authors'])
    # create list of authors from response(all authors in db)
    author_list = []
    for author in authors:
        author_list.append(author.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve error message and author_list matches expected_list if form submission fail
    assert response_message.message == 'Sorry, same author already exists'
    expected_list = ['サン・テグジュペリ', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)


def test_author_edit_to_not_existing_name(setup_author_objects, client):
    """Author will be updated if same name don't exists"""
    # POST from author-edit('サン・テグジュペリ') page
    a1 = Author.objects.get(name='サン・テグジュペリ')
    response = client.post(reverse('book:author edit', kwargs={'id': a1.id}), {
        'name': '東野圭吾'}, follow=True)
    # retrieve 'authors' context from response
    authors = list(response.context['authors'])
    # create list of authors from response(all authors in db)
    author_list = []
    for author in authors:
        author_list.append(author.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve success message and author_list matches expected_list if form submission success
    assert response_message.message == 'Update submission succesfull'
    expected_list = ['東野圭吾', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)


def test_author_edit_existing_name(setup_author_objects, client):
    """Author won't be updated if same name exists"""
    # POST from author-edit(サン・テグジュペリ') page
    a1 = Author.objects.get(name='サン・テグジュペリ')
    response = client.post(reverse('book:author edit', kwargs={'id': a1.id}), {
        'name': '池澤夏樹'}, follow=True)
    # retrieve 'authors' context from response
    authors = list(response.context['authors'])
    # create list of authors from response(all authors in db)
    author_list = []
    for author in authors:
        author_list.append(author.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve error message and author_list matches expected_list if form submission fail
    assert response_message.message == 'Sorry, same author already exists'
    expected_list = ['サン・テグジュペリ', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)
