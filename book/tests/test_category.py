import pytest
from django.urls import reverse
from book.models import Category


@pytest.fixture()
def setup_category_objects():
    # Set up Category('Novel' and 'Deisgn')
    return Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])


def test_category_register_with_not_existing_name(setup_category_objects, client):
    """Category will be registred if same name don't exists"""
    # create form data for POST
    form_data = {'name': 'Programming'}
    # POST from cateogory-register page
    response = client.post('/category-register/', form_data, follow=True)
    # retrieve 'categories' context from response
    categories = list(response.context['categories'])
    # create list of categories from response(all categories in db)
    category_list = []
    for category in categories:
        category_list.append(category.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve success message and category_list matches expected_list if form submission success
    assert response_message.message == 'Form submission successful'
    expected_list = ['Novel', 'Design', 'Programming']
    assert sorted(expected_list) == sorted(category_list)


def test_category_register_with_existing_name(setup_category_objects, client):
    """Category won't be registred if same name exists"""
    # create form data for POST
    form_data = {'name': 'Novel'}
    # POST from cateogory-register page
    response = client.post('/category-register/', form_data, follow=True)
    # retrieve 'categories' context from response
    categories = list(response.context['categories'])
    # create list of categories from response(all categories in db)
    category_list = []
    for category in categories:
        category_list.append(category.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve error message and category_list matches expected_list if form submission fail
    assert response_message.message == 'Sorry, same category already exists'
    expected_list = ['Novel', 'Design']
    assert sorted(expected_list) == sorted(category_list)


def test_category_edit_to_not_existing_name(setup_category_objects, client):
    """Category will be updated if same name don't exists"""
    # POST from cateogory-edit('Novel') page
    category = Category.objects.get(name='Novel')
    response = client.post(reverse('book:category edit', kwargs={'id': category.id}), {
        'name': 'Python'}, follow=True)
    # retrieve 'categories' context from response
    categories = list(response.context['categories'])
    # create list of categories from response(all categories in db)
    category_list = []
    for category in categories:
        category_list.append(category.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve success message and category_list matches expected_list if form submission success
    assert response_message.message == 'Update submission succesfull'
    expected_list = ['Design', 'Python']
    assert sorted(expected_list) == sorted(category_list)


def test_category_edit_existing_name(setup_category_objects, client):
    """Category won't be updated if same name exists"""
    # POST from cateogory-edit('Novel') page
    category = Category.objects.get(name='Novel')
    response = client.post(reverse('book:category edit', kwargs={'id': category.id}), {
        'name': 'Design'}, follow=True)
    # retrieve 'categories' context from response
    categories = list(response.context['categories'])
    # create list of categories from response(all categories in db)
    category_list = []
    for category in categories:
        category_list.append(category.name)
    # retrieve list of messages from response
    messages = list(response.context['messages'])
    # get message set in views.py
    response_message = messages[0]
    # Retrieve error message and category_list matches expected_list if form submission fail
    assert response_message.message == 'Sorry, same category already exists'
    expected_list = ['Novel', 'Design']
    assert sorted(expected_list) == sorted(category_list)
