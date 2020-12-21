import pytest
from django.urls import reverse
from book.models import Book, Author, Category
from book.forms import BookForm, AuthorForm, CategoryForm


# test1 register(title not duplicate)
# test2 register(all duplicate)
# test3 register(title duplicate, other not)
# test4 register(title and author duplicate, other not)


class TestCategoryFunction():
    #
    @pytest.fixture()
    def setup_category(self):
        return Category.objects.bulk_create([
            Category(name='Novel'),
            Category(name='Design')
        ])

    def test_category_register_case1(self, setup_category, client):
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

    def test_category_register_case2(self, setup_category, client):
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

    def test_category_edit_case1(self, setup_category, client):
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

    def test_category_edit_case2(self, setup_category, client):
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


class TestAuthorFunction():
    @pytest.fixture()
    def setup_author(self):
        return Author.objects.bulk_create([
            Author(name='サン・テグジュペリ'),
            Author(name='池澤夏樹')
        ])

    def test_author_register_case1(self, setup_author, client):
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

    def test_author_register_case2(self, setup_author, client):
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

    def test_author_edit_case1(self, setup_author, client):
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

    def test_author_edit_case2(self, setup_author, client):
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


class TestBookFunction():
    @pytest.fixture()
    def setup_book(self):
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
        c1 = Category.objects.get(name='Novel')
        # c2 = Category.objects.get(name='Design')
        a1 = Author.objects.get(name='サン・テグジュペリ')
        # a2 = Author.objects.get(name='池澤 夏樹')
        b1.categories.add(c1)
        b1.authors.add(a1)
        return b1

    def test_demo(self, setup_book, client):
        r = client.get('/book-register/')
        con = r.context
        widget = r.context['widget']
        print(con)
        print(widget)

        form_data = {
            'title': '星の王子様',
            'published_date': '1995-12-28',
            'categories': [1],
            'authors': [1]
        }
        response = client.post('/book-register/', form_data)
        print(response)
        # assert form_data.is_valid() == True
        assert response.url == '/book-shelf/'
