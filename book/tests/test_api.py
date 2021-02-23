import pytest
from django.urls import reverse
from book.models import Book, Author, Category
import json


@pytest.fixture()
def setup_book_objects():
    Category.objects.bulk_create(
        [Category(name="Category1"), Category(name="Category2")]
    )
    Author.objects.bulk_create([Author(name="Author1"), Author(name="Author2")])
    c1 = Category.objects.get(name="Category1")
    c2 = Category.objects.get(name="Category2")
    a1 = Author.objects.get(name="Author1")
    a2 = Author.objects.get(name="Author2")
    b1 = Book(title="Book1", published_date="2006-03-28")
    b1.save()
    b1.categories.add(c1)
    b1.authors.add(a1, a2)
    b2 = Book(title="Book2", published_date="2015-08-20")
    b2.save()
    b2.categories.add(c2)
    b2.authors.add(a1)


def test_get_book_list_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response = client.get("/api/books")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    get_response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        [
            {
                "id": b1_pk,
                "title": "Book1",
                "published_date": "2006-03-28",
                "categories": [{"id": c1_pk, "name": "Category1"}],
                "authors": [
                    {"id": a1_pk, "name": "Author1"},
                    {"id": a2_pk, "name": "Author2"},
                ],
            },
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [{"id": a1_pk, "name": "Author1"}],
            },
        ]
    )
    assert expected_data == get_response_data


def test_post_book_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {
        "id": None,
        "title": "Book3",
        "published_date": "2015-08-20",
        "categories": [{"id": c1_pk, "name": "Category1"}],
        "authors": [{"id": a1_pk, "name": "Author1"}, {"id": a2_pk, "name": "Author2"}],
    }
    post_response_status = client.post(
        "/api/books", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    b3_pk = Book.objects.get(title="Book3").pk
    expected_data = json.dumps(
        [
            {
                "id": b1_pk,
                "title": "Book1",
                "published_date": "2006-03-28",
                "categories": [{"id": c1_pk, "name": "Category1"}],
                "authors": [
                    {"id": a1_pk, "name": "Author1"},
                    {"id": a2_pk, "name": "Author2"},
                ],
            },
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [{"id": a1_pk, "name": "Author1"}],
            },
            {
                "id": b3_pk,
                "title": "Book3",
                "published_date": "2015-08-20",
                "categories": [{"id": c1_pk, "name": "Category1"}],
                "authors": [
                    {"id": a1_pk, "name": "Author1"},
                    {"id": a2_pk, "name": "Author2"},
                ],
            },
        ]
    )
    get_response_data = client.get("/api/books").content.decode("utf-8")
    assert expected_data == get_response_data


def test_get_book_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response_data = client.get("/api/books/" + str(b1_pk)).content.decode("utf-8")
    expected_data = json.dumps(
        {
            "id": b1_pk,
            "title": "Book1",
            "published_date": "2006-03-28",
            "categories": [{"id": c1_pk, "name": "Category1"}],
            "authors": [
                {"id": a1_pk, "name": "Author1"},
                {"id": a2_pk, "name": "Author2"},
            ],
        }
    )
    assert expected_data == get_response_data


def test_put_book_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    form_data = {
        "id": b1_pk,
        "title": "Book1",
        "published_date": "1995-03-28",
        "categories": [{"id": c1_pk, "name": "Category1"}],
        "authors": [{"id": a1_pk, "name": "Author1"}],
    }
    put_response_status = client.put(
        "/api/books/" + str(b1_pk),
        data=json.dumps(form_data),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    expected_data = json.dumps(
        {
            "id": b1_pk,
            "title": "Book1",
            "published_date": "1995-03-28",
            "categories": [{"id": c1_pk, "name": "Category1"}],
            "authors": [{"id": a1_pk, "name": "Author1"}],
        }
    )
    get_response_data = client.get("/api/books/" + str(b1_pk)).content.decode("utf-8")
    assert expected_data == get_response_data


def test_delete_book_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    delete_response_status = client.delete("/api/books/" + str(b1_pk)).status_code
    assert delete_response_status == 204
    get_response_data = client.get("/api/books").content.decode("utf-8")
    expected_data = json.dumps(
        [
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [{"id": a1_pk, "name": "Author1"}],
            }
        ]
    )
    assert expected_data == get_response_data


def test_get_author_list_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response = client.get("/api/authors")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        [
            {"id": a1_pk, "name": "Author1"},
            {"id": a2_pk, "name": "Author2"},
        ]
    )
    assert expected_data == response_data


def test_post_author_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": None, "name": "Author3"}
    post_response_status = client.post(
        "/api/authors", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    a3_pk = Author.objects.get(name="Author3").pk
    expected_data = json.dumps(
        [
            {"id": a1_pk, "name": "Author1"},
            {"id": a2_pk, "name": "Author2"},
            {"id": a3_pk, "name": "Author3"},
        ]
    )
    get_response_data = client.get("/api/authors").content.decode("utf-8")
    assert expected_data == get_response_data


def test_get_author_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    get_response_data = client.get("/api/authors/" + str(a1_pk)).content.decode("utf-8")
    expected_data = {"id": a1_pk, "name": "Author1"}
    expected_data = json.dumps(expected_data)
    assert expected_data == get_response_data


def test_put_author_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": a1_pk, "name": "Update Author"}
    put_response_status = client.put(
        "/api/authors/" + str(a1_pk),
        data=json.dumps(form_data),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    authors_get_response_data = client.get("/api/authors").content.decode("utf-8")
    authors_expected_data = json.dumps(
        [
            {"id": a2_pk, "name": "Author2"},
            {"id": a1_pk, "name": "Update Author"},
        ]
    )
    assert authors_expected_data == authors_get_response_data
    books_expected_data = json.dumps(
        {
            "id": b1_pk,
            "title": "Book1",
            "published_date": "2006-03-28",
            "categories": [{"id": c1_pk, "name": "Category1"}],
            "authors": [
                {"id": a2_pk, "name": "Author2"},
                {"id": a1_pk, "name": "Update Author"},
            ],
        }
    )
    books_get_response_data = client.get("/api/books/" + str(b1_pk)).content.decode(
        "utf-8"
    )
    assert books_expected_data == books_get_response_data


def test_delete_author_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    delete_response_status = client.delete("/api/authors/" + str(a1_pk)).status_code
    assert delete_response_status == 204
    authors_get_response_data = client.get("/api/authors").content.decode("utf-8")
    authors_expected_data = json.dumps([{"id": a2_pk, "name": "Author2"}])
    assert authors_expected_data == authors_get_response_data
    books_get_response_data = client.get("/api/books").content.decode("utf-8")
    books_expected_data = json.dumps(
        [
            {
                "id": b1_pk,
                "title": "Book1",
                "published_date": "2006-03-28",
                "categories": [{"id": c1_pk, "name": "Category1"}],
                "authors": [
                    {"id": a2_pk, "name": "Author2"},
                ],
            },
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [],
            },
        ]
    )
    assert books_expected_data == books_get_response_data


def test_get_category_list_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    get_response = client.get("/api/categories")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        [
            {"id": c1_pk, "name": "Category1"},
            {"id": c2_pk, "name": "Category2"},
        ]
    )
    assert expected_data == response_data


def test_post_category_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    form_data = {"id": None, "name": "Category3"}
    post_response_status = client.post(
        "/api/categories", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    c3_pk = Category.objects.get(name="Category3").pk
    expected_data = json.dumps(
        [
            {"id": c1_pk, "name": "Category1"},
            {"id": c2_pk, "name": "Category2"},
            {"id": c3_pk, "name": "Category3"},
        ]
    )
    get_response_data = client.get("/api/categories").content.decode("utf-8")
    assert expected_data == get_response_data


def test_get_category_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    get_response_data = client.get("/api/categories/" + str(c1_pk)).content.decode(
        "utf-8"
    )
    expected_data = {"id": c1_pk, "name": "Category1"}
    expected_data = json.dumps(expected_data)
    assert expected_data == get_response_data


def test_put_category_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": c1_pk, "name": "Update Category"}
    put_response_status = client.put(
        "/api/categories/" + str(c1_pk),
        data=json.dumps(form_data),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    categories_get_response_data = client.get("/api/categories").content.decode("utf-8")
    categories_expected_data = json.dumps(
        [
            {"id": c2_pk, "name": "Category2"},
            {"id": c1_pk, "name": "Update Category"},
        ]
    )
    assert categories_expected_data == categories_get_response_data
    books_expected_data = json.dumps(
        {
            "id": b1_pk,
            "title": "Book1",
            "published_date": "2006-03-28",
            "categories": [{"id": c1_pk, "name": "Update Category"}],
            "authors": [
                {"id": a1_pk, "name": "Author1"},
                {"id": a2_pk, "name": "Author2"},
            ],
        }
    )
    books_get_response_data = client.get("/api/books/" + str(b1_pk)).content.decode(
        "utf-8"
    )
    assert books_expected_data == books_get_response_data


def test_delete_category_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    delete_response_status = client.delete("/api/categories/" + str(c1_pk)).status_code
    assert delete_response_status == 204
    categories_get_response_data = client.get("/api/categories").content.decode("utf-8")
    categories_expected_data = json.dumps([{"id": c2_pk, "name": "Category2"}])
    assert categories_expected_data == categories_get_response_data
    books_get_response_data = client.get("/api/books").content.decode("utf-8")
    books_expected_data = json.dumps(
        [
            {
                "id": b1_pk,
                "title": "Book1",
                "published_date": "2006-03-28",
                "categories": [],
                "authors": [
                    {"id": a1_pk, "name": "Author1"},
                    {"id": a2_pk, "name": "Author2"},
                ],
            },
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [{"id": a1_pk, "name": "Author1"}],
            },
        ]
    )
    assert books_expected_data == books_get_response_data
