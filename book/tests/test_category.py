import pytest
from django.urls import reverse
from book.models import Category


@pytest.fixture()
def setup_category_objects():
    return Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])


# 同じカテゴリーが存在しない場合は登録が出来ることをテスト
def test_category_register_with_not_existing_name(setup_category_objects, client):
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


# 同じカテゴリーが存在する場合は登録が拒否されることをテスト
def test_category_register_with_existing_name(setup_category_objects, client):
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


# 編集後の著者が既に存在していなければ編集が完了することをテスト
def test_category_edit_to_not_existing_name(setup_category_objects, client):
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


# 編集後の著者が既に存在していれば編集が拒否されることをテスト
def test_category_edit_existing_name(setup_category_objects, client):
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
