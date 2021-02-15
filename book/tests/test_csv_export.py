import csv
import io

import pytest
from book.models import Author, Book, Category


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


def test_csv_export(setup_book_objects, client):
    response = client.post('/book-shelf/', {'csv-export': 'True'})
    content = response.content.decode('utf-8')
    cvs_reader = csv.reader(io.StringIO(content))
    download_data = list(cvs_reader)
    header = download_data.pop(0)

    expected_header = ['No.', 'Title', 'Published Date', 'Author', 'Category']
    expected_data = [
        ['1', '星の王子様', '2006-03-28', 'サン・テグジュペリ, 池澤夏樹', 'Novel'],
        ['2', '人間の大地', '2015-08-20', 'サン・テグジュペリ', 'Novel']
    ]
    assert header == expected_header
    assert download_data == expected_data
