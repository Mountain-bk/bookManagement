import pytest
from django.urls import reverse
from book.models import Category


@pytest.fixture()
def setup_category_objects():
    return Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])


def test_category_register_with_not_existing_name(setup_category_objects, client):
    """同じカテゴリーが存在しない場合は登録が出来ることをテスト"""
    form_data = {'name': 'Programming'}
    response = client.post('/category-register/', form_data, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Form submission successful'
    expected_list = ['Novel', 'Design', 'Programming']
    assert sorted(expected_list) == sorted(category_list)


def test_category_register_with_existing_name(setup_category_objects, client):
    """同じカテゴリーが存在する場合は登録が拒否されることをテスト"""
    form_data = {'name': 'Novel'}
    response = client.post('/category-register/', form_data, follow=True)
    categories = list(response.context['categories'])
    category_list = []
    for category in categories:
        category_list.append(category.name)
    messages = list(response.context['messages'])
    response_message = messages[0]
    assert response_message.message == 'Sorry, same category already exists'
    expected_list = ['Novel', 'Design']
    assert sorted(expected_list) == sorted(category_list)


def test_category_edit_to_not_existing_name(setup_category_objects, client):
    """編集後の著者が重複していなければ編集が完了することをテスト"""
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
    expected_list = ['Design', 'Python']
    assert sorted(expected_list) == sorted(category_list)


def test_category_edit_existing_name(setup_category_objects, client):
    """編集後の著者の名前が重複していれば拒否されることをテスト"""
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
    expected_list = ['Novel', 'Design']
    assert sorted(expected_list) == sorted(category_list)
