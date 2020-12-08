import pytest
from book.models import Book, Author, Category
from book.forms import BookForm


# test1 register(title not duplicate)
# test2 register(all duplicate)
# test3 register(title duplicate, other not)
# test4 register(title and author duplicate, other not)
# test5 edit(title not duplicate)
# test6 edit(all duplicate)
# test7 edit(title duplicate, other not)
# test8 edit(title and author duplicate, other not)


@pytest.fixture()
def set_prerequisites():
    # Create Category objects
    Category.objects.bulk_create([
        Category(name='Novel'),
        Category(name='Design')
    ])
    # Create Author objects
    Author.objects.bulk_create([
        Author(name='サン・テグジュペリ'),
        Author(name='池澤 夏樹')
    ])
    # Create Book object
    # title='星の王子様'
    # published date='2006-03-28'
    # categories='Novel'
    # authors='サン・テグジュペリ', '池澤 夏樹'
    b1 = Book(title='星の王子様',
              published_date='2006-03-28')
    b1.save()
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤 夏樹')
    b1.categories.add(c1)
    b1.authors.add(a1, a2)


def test_book_register_form_1(set_prerequisites):
    """Book register should completed"""
    # GIVEN set_prerequisites
    # WHEN title is not duplicate
    # THEN existing Book will be 2
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    b2 = BookForm(
        {
            'title': '人間の大地',
            'published_date': '2015-08-20',
            'categories': [c1],
            'authors': [a1]
        }
    )
    if b2.is_valid():
        b2.save()
    else:
        pass
    assert Book.objects.count() == 2


def test_book_register_form_2(set_prerequisites):
    """Book register should be error"""
    # GIVEN set_prerequisites
    # WHEN all atributes are completely duplicate
    # THEN existing Book will be 1
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤 夏樹')
    b2 = BookForm(
        {
            'title': '星の王子様',
            'published_date': '2006-03-28',
            'categories': [c1],
            'authors': [a1, a2]
        }
    )
    if b2.is_valid():
        b2.save()
    else:
        pass
    assert Book.objects.count() == 1


def test_book_register_form_3(set_prerequisites):
    """Book register should be completed"""
    # GIVEN set_prerequisites
    # WHEN title is duplicate, but authors are not completely duplicated
    # THEN existing Book will be 2
    c1 = Category.objects.get(name='Novel')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    b2 = BookForm(
        {
            'title': '星の王子様',
            'published_date': '2006-03-28',
            'categories': [c1],
            'authors': [a1]
        }
    )
    if b2.is_valid():
        b2.save()
    else:
        pass
    assert Book.objects.count() == 2


def test_book_register_form_4(set_prerequisites):
    """Book register should be error"""
    # GIVEN set_prerequisites
    # WHEN title and authors are completely duplicate,
    # but categories and pub_date are not duplicate
    # THEN existing Book will be 1
    c2 = Category.objects.get(name='Design')
    a1 = Author.objects.get(name='サン・テグジュペリ')
    a2 = Author.objects.get(name='池澤 夏樹')
    b2 = BookForm(
        {
            'title': '星の王子様',
            'published_date': '1995-12-28',
            'categories': [c2],
            'authors': [a1, a2]
        }
    )
    if b2.is_valid():
        b2.save()
    else:
        pass
    assert Book.objects.count() == 1
