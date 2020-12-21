import pytest
from django.urls import reverse
from book.models import Category


@pytest.fixture()
def setup_category():
    return Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])


def test_category_register_case1(setup_category, client):
    form_data = {'name': 'Programming'}
    response = client.post('/category-register/', form_data, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Form submission successful'
    assert 'Programming' in category_list


def test_category_register_case2(setup_category, client):
    form_data = {'name': 'Novel'}
    response = client.post('/category-register/', form_data, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same category already exists'
    assert category_list.count('Novel') == 1


def test_category_edit_case1(setup_category, client):
    category = Category.objects.get(name='Novel')
    response = client.post(reverse('book:category edit', kwargs={'id': category.id}), {
        'name': 'Python'}, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Update submission succesfull'
    assert 'Design', 'Python' in category_list == True


def test_category_edit_case2(setup_category, client):
    category = Category.objects.get(name='Novel')
    response = client.post(reverse('book:category edit', kwargs={'id': category.id}), {
        'name': 'Design'}, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same category already exists'
    assert category_list.count('Novel') == 1
