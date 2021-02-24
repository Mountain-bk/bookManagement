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


# Test retrieving a list of book details
def test_get_book_list_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response = client.get("/books/")
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
        ],
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# Test creating a new book
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
        "/books/", data=json.dumps(form_data), content_type="application/json"
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
        ],
        separators=(",", ":"),
    )
    get_response_data = client.get("/books/").content.decode("utf-8")
    assert expected_data == get_response_data


# Test retrieving individual book detail
def test_get_book_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response_data = client.get("/books/" + str(b1_pk) + "/").content.decode("utf-8")
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
        },
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# Test updating individual book details
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
        "/books/" + str(b1_pk) + "/",
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
        },
        separators=(",", ":"),
    )
    get_response_data = client.get("/books/" + str(b1_pk) + "/").content.decode("utf-8")
    assert expected_data == get_response_data


# Test deleting individual book
def test_delete_book_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    delete_response_status = client.delete("/books/" + str(b1_pk) + "/").status_code
    assert delete_response_status == 204
    get_response_data = client.get("/books/").content.decode("utf-8")
    expected_data = json.dumps(
        [
            {
                "id": b2_pk,
                "title": "Book2",
                "published_date": "2015-08-20",
                "categories": [{"id": c2_pk, "name": "Category2"}],
                "authors": [{"id": a1_pk, "name": "Author1"}],
            }
        ],
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# Test retrieving a list of author details
def test_get_author_list_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    get_response = client.get("/authors/")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        [
            {"id": a1_pk, "name": "Author1"},
            {"id": a2_pk, "name": "Author2"},
        ],
        separators=(",", ":"),
    )
    assert expected_data == response_data


# Test creating a new author
def test_post_author_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": None, "name": "Author3"}
    post_response_status = client.post(
        "/authors/", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    a3_pk = Author.objects.get(name="Author3").pk
    expected_data = json.dumps(
        [
            {"id": a1_pk, "name": "Author1"},
            {"id": a2_pk, "name": "Author2"},
            {"id": a3_pk, "name": "Author3"},
        ],
        separators=(",", ":"),
    )
    get_response_data = client.get("/authors/").content.decode("utf-8")
    assert expected_data == get_response_data


# Test retrieving individual author detail
def test_get_author_detail_api(setup_book_objects, client):
    a1_pk = Author.objects.get(name="Author1").pk
    get_response_data = client.get("/authors/" + str(a1_pk) + "/").content.decode(
        "utf-8"
    )
    expected_data = {"id": a1_pk, "name": "Author1"}
    expected_data = json.dumps(
        expected_data,
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# Test updating individual author details
def test_put_author_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": a1_pk, "name": "Update Author"}
    put_response_status = client.put(
        "/authors/" + str(a1_pk) + "/",
        data=json.dumps(form_data),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    authors_get_response_data = client.get("/authors/").content.decode("utf-8")
    authors_expected_data = json.dumps(
        [
            {"id": a2_pk, "name": "Author2"},
            {"id": a1_pk, "name": "Update Author"},
        ],
        separators=(",", ":"),
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
        },
        separators=(",", ":"),
    )
    books_get_response_data = client.get("/books/" + str(b1_pk) + "/").content.decode(
        "utf-8"
    )
    assert books_expected_data == books_get_response_data


# Test deleting individual author
def test_delete_author_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    delete_response_status = client.delete("/authors/" + str(a1_pk) + "/").status_code
    assert delete_response_status == 204
    authors_get_response_data = client.get("/authors/").content.decode("utf-8")
    authors_expected_data = json.dumps(
        [{"id": a2_pk, "name": "Author2"}],
        separators=(",", ":"),
    )
    assert authors_expected_data == authors_get_response_data
    books_get_response_data = client.get("/books/").content.decode("utf-8")
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
        ],
        separators=(",", ":"),
    )
    assert books_expected_data == books_get_response_data


# Test retrieving a list of category details
def test_get_category_list_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    get_response = client.get("/categories/")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        [
            {"id": c1_pk, "name": "Category1"},
            {"id": c2_pk, "name": "Category2"},
        ],
        separators=(",", ":"),
    )
    assert expected_data == response_data


# Test creating a new category
def test_post_category_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    form_data = {"id": None, "name": "Category3"}
    post_response_status = client.post(
        "/categories/", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    c3_pk = Category.objects.get(name="Category3").pk
    expected_data = json.dumps(
        [
            {"id": c1_pk, "name": "Category1"},
            {"id": c2_pk, "name": "Category2"},
            {"id": c3_pk, "name": "Category3"},
        ],
        separators=(",", ":"),
    )
    get_response_data = client.get("/categories/").content.decode("utf-8")
    assert expected_data == get_response_data


# Test retrieving individual category detail
def test_get_category_detail_api(setup_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    get_response_data = client.get("/categories/" + str(c1_pk) + "/").content.decode(
        "utf-8"
    )
    expected_data = json.dumps(
        {"id": c1_pk, "name": "Category1"},
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# Test updating individual category details
def test_put_category_detail_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    form_data = {"id": c1_pk, "name": "Update Category"}
    put_response_status = client.put(
        "/categories/" + str(c1_pk) + "/",
        data=json.dumps(form_data),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    categories_get_response_data = client.get("/categories/").content.decode("utf-8")
    categories_expected_data = json.dumps(
        [
            {"id": c2_pk, "name": "Category2"},
            {"id": c1_pk, "name": "Update Category"},
        ],
        separators=(",", ":"),
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
        },
        separators=(",", ":"),
    )
    books_get_response_data = client.get("/books/" + str(b1_pk) + "/").content.decode(
        "utf-8"
    )
    assert books_expected_data == books_get_response_data


# Test deleting individual category
def test_delete_category_api(setup_book_objects, client):
    b1_pk = Book.objects.get(title="Book1").pk
    b2_pk = Book.objects.get(title="Book2").pk
    c1_pk = Category.objects.get(name="Category1").pk
    c2_pk = Category.objects.get(name="Category2").pk
    a1_pk = Author.objects.get(name="Author1").pk
    a2_pk = Author.objects.get(name="Author2").pk
    delete_response_status = client.delete(
        "/categories/" + str(c1_pk) + "/"
    ).status_code
    assert delete_response_status == 204
    categories_get_response_data = client.get("/categories/").content.decode("utf-8")
    categories_expected_data = json.dumps(
        [{"id": c2_pk, "name": "Category2"}],
        separators=(",", ":"),
    )
    assert categories_expected_data == categories_get_response_data
    books_get_response_data = client.get("/books/").content.decode("utf-8")
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
        ],
        separators=(",", ":"),
    )
    assert books_expected_data == books_get_response_data
