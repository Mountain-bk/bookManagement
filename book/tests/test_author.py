import pytest
from django.urls import reverse
from book.models import Author


@pytest.fixture()
def setup_author_objects():
    return Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤夏樹')
    ])


# 同じ著者が存在しない場合は登録が出来ることをテスト
def test_author_register_with_not_existing_name(setup_author_objects, client):
    form_data = {'name': '村上春樹'}
    response = client.post('/author-register/', form_data, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Form submission successful'
    expected_list = ['サン・テグジュペリ', '池澤夏樹', '村上春樹']
    assert sorted(expected_list) == sorted(author_list)


# 同じ著者が存在する場合は登録が拒否されることをテスト
def test_author_register_with_existing_name(setup_author_objects, client):
    form_data = {'name': 'サン・テグジュペリ'}
    response = client.post('/author-register/', form_data, follow=True)
    authors = list(response.context['authors'])
    author_list = []
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same author already exists'
    expected_list = ['サン・テグジュペリ', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)


# 編集後の著者が既に存在していなければ編集が完了することをテスト
def test_author_edit_to_not_existing_name(setup_author_objects, client):
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
    expected_list = ['東野圭吾', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)


# 編集後の著者が既に存在していれば編集が拒否されることをテスト
def test_author_edit_existing_name(setup_author_objects, client):
    a1 = Author.objects.get(name='サン・テグジュペリ')
    response = client.post(reverse('book:author edit', kwargs={'id': a1.id}), {
        'name': '池澤夏樹'}, follow=True)
    authors = list(response.context['authors'])
    author_list =
    for author in authors:
        author_list.append(author.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same author already exists'
    expected_list = ['サン・テグジュペリ', '池澤夏樹']
    assert sorted(expected_list) == sorted(author_list)
