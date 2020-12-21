import pytest
from django.urls import reverse
from book.models import Author


@pytest.fixture()
def setup_author():
    return Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])


def test_author_register_case1(setup_author, client):
    form_data = {'name': '村上春樹'}
    response = client.post('/author-register/', form_data, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Form submission successful'
    assert '村上春樹' in author_list


def test_author_register_case2(setup_author, client):
    form_data = {'name': 'サン・テグジュペリ'}
    response = client.post('/author-register/', form_data, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same author already exists'
    assert author_list.count('サン・テグジュペリ') == 1


def test_author_edit_case1(setup_author, client):
    a1 = Author.objects.get(name='サン・テグジュペリ')
    response = client.post(reverse('book:author edit', kwargs={'id': a1.id}), {
        'name': '東野圭吾'}, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Update submission succesfull'
    assert '池澤夏樹', '東野圭吾' in author_list == True


def test_author_edit_case2(setup_author, client):
    a1 = Author.objects.get(name='サン・テグジュペリ')
    response = client.post(reverse('book:author edit', kwargs={'id': a1.id}), {
        'name': '池澤夏樹'}, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same author already exists'
    assert author_list.count('池澤夏樹') == 1
