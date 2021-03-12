import json
import random

import pytest
from book.models import Author, Book, Category


# 単数書籍をセットアップ
@pytest.fixture()
def setup_book_object():
    c1 = Category.objects.create(name="Category1")
    a1 = Author.objects.create(name="Author1")
    b1 = Book(title="Book1", published_date="2006-03-28")
    b1.save()
    b1.categories.add(c1)
    b1.authors.add(a1)


# ユニークなタイトルの書籍を複数セットアップ
@pytest.fixture()
def setup_multiple_book_objects(request):
    c1 = Category.objects.create(name="Category1")
    a1 = Author.objects.create(name="Author1")
    for i in range(request.param):
        b1 = Book(title="Book" + str(i + 1), published_date="2006-03-28")
        b1.save()
        b1.categories.add(c1)
        b1.authors.add(a1)


# タイトルが同じ書籍を複数セットアップ
@pytest.fixture()
def setup_multiple_same_title_book_objects(request):
    c1 = Category.objects.create(name="Category1")
    a1 = Author.objects.create(name="Author1")
    for i in range(request.param):
        b1 = Book(title="Book", published_date="2006-03-28")
        b1.save()
        b1.categories.add(c1)
        b1.authors.add(a1)


# 複数の書籍を一覧で取得出来ることをテスト(テストする書籍数：5, 10, 50 100)
@pytest.mark.parametrize("setup_multiple_book_objects", [5, 10, 50, 100], indirect=True)
def test_get_book_list_detail_api(setup_multiple_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    response = client.get("/books/")
    get_response_status = response.status_code
    assert get_response_status == 200
    get_response_data = response.content.decode("utf-8")
    book_amount = len(Book.objects.all())
    generate_expected_data = []
    for i in range(book_amount):
        x = {
            "id": Book.objects.get(title="Book" + str(i + 1)).pk,
            "title": "Book" + str(i + 1),
            "published_date": "2006-03-28",
            "categories": [
                {"id": c1_pk, "name": "Category1"},
            ],
            "authors": [
                {"id": a1_pk, "name": "Author1"},
            ],
        }
        generate_expected_data.append(x)
    expected_data = json.dumps(
        generate_expected_data,
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# 単数書籍の登録が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "title": "Book1",
                "published_date": "2015-08-20",
                "categories": [{"name": "Category1"}],
                "authors": [{"name": "Author1"}, {"name": "Author2"}],
            },
            {
                "id": 1,
                "title": "Book1",
                "published_date": "2015-08-20",
                "categories": [{"id": 1, "name": "Category1"}],
                "authors": [
                    {"id": 1, "name": "Author1"},
                    {"id": 2, "name": "Author2"},
                ],
            },
        ),
        (
            {
                "id": None,
                "title": "日本語タイトル",
                "published_date": "2015-08-20",
                "categories": [
                    {"name": "カテゴリ１"},
                    {"name": "カテゴリ２"},
                ],
                "authors": [{"name": "著者１"}],
            },
            {
                "id": 2,
                "title": "日本語タイトル",
                "published_date": "2015-08-20",
                "categories": [
                    {"id": 2, "name": "カテゴリ１"},
                    {"id": 3, "name": "カテゴリ２"},
                ],
                "authors": [
                    {"id": 3, "name": "著者１"},
                ],
            },
        ),
        (
            {
                "id": None,
                "title": "Mix半角全角",
                "published_date": "2015-08-20",
                "categories": [{"name": "Mixカテゴリ半角全角"}],
                "authors": [{"name": "Mix著者半角全角No.1"}, {"name": "Mix著者半角全角No.2"}],
            },
            {
                "id": 1,
                "title": "Mix半角全角",
                "published_date": "2015-08-20",
                "categories": [{"id": 1, "name": "Mixカテゴリ半角全角"}],
                "authors": [
                    {"id": 1, "name": "Mix著者半角全角No.1"},
                    {"id": 2, "name": "Mix著者半角全角No.2"},
                ],
            },
        ),
    ],
)
def test_post_book_detail_api(test_input, expected, client):
    post_response_status = client.post(
        "/books/", data=json.dumps(test_input), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    expected["id"] = Book.objects.get(title=expected["title"]).pk
    for category in expected["categories"]:
        category["id"] = Category.objects.get(name=category["name"]).pk
    for author in expected["authors"]:
        author["id"] = Author.objects.get(name=author["name"]).pk
    expected_data = json.dumps([expected], separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/books/").content.decode("utf-8")
    assert expected_data == get_response_data


# 単数書籍の編集が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "title": "Update Title",
                "published_date": "2015-08-20",
                "categories": [{"name": "Update Category"}],
                "authors": [{"name": "Update Author"}],
            },
            {
                "id": 1,
                "title": "Update Title",
                "published_date": "2015-08-20",
                "categories": [{"id": 1, "name": "Update Category"}],
                "authors": [
                    {"id": 1, "name": "Update Author"},
                ],
            },
        ),
        (
            {
                "id": None,
                "title": "アップデートタイトル",
                "published_date": "2015-08-20",
                "categories": [{"name": "カテゴリ１"}, {"name": "カテゴリ２"}],
                "authors": [{"name": "著者１"}, {"name": "著者２"}],
            },
            {
                "id": 2,
                "title": "アップデートタイトル",
                "published_date": "2015-08-20",
                "categories": [{"id": 1, "name": "カテゴリ１"}, {"id": 2, "name": "カテゴリ２"}],
                "authors": [
                    {"id": 3, "name": "著者１"},
                    {"id": 4, "name": "著者２"},
                ],
            },
        ),
        (
            {
                "id": None,
                "title": "Update半角全角Title",
                "published_date": "2015-08-20",
                "categories": [{"name": "Updateカテゴリ１"}, {"name": "Updateカテゴリ２"}],
                "authors": [{"name": "Update著者１"}, {"name": "Update著者２"}],
            },
            {
                "id": 2,
                "title": "Update半角全角Title",
                "published_date": "2015-08-20",
                "categories": [
                    {"id": 1, "name": "Updateカテゴリ１"},
                    {"id": 2, "name": "Updateカテゴリ２"},
                ],
                "authors": [
                    {"id": 3, "name": "Update著者１"},
                    {"id": 4, "name": "Update著者２"},
                ],
            },
        ),
    ],
)
def test_put_book_detail_api(setup_book_object, test_input, expected, client):
    b1_pk = Book.objects.get(title="Book1").pk
    test_input["id"] = b1_pk
    put_response_status = client.put(
        "/books/" + str(b1_pk) + "/",
        data=json.dumps(test_input),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    expected["id"] = b1_pk
    for category in expected["categories"]:
        category["id"] = Category.objects.get(name=category["name"]).pk
    for author in expected["authors"]:
        author["id"] = Author.objects.get(name=author["name"]).pk
    expected_data = json.dumps(expected, separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/books/" + str(b1_pk) + "/").content.decode("utf-8")
    assert expected_data == get_response_data


# 複数書籍から指定した書籍が取得出来ることをテスト(テストする書籍数：5, 10, 50 100)
# 正しいIDを取得していることを確認するために同じタイトルの書籍を複数セットアップ
@pytest.mark.parametrize(
    "setup_multiple_same_title_book_objects", [5, 10, 50, 100], indirect=True
)
def test_get_book_detail_api(setup_multiple_same_title_book_objects, client):
    c1_pk = Category.objects.get(name="Category1").pk
    a1_pk = Author.objects.get(name="Author1").pk
    response = client.get("/books/")
    get_response_status = response.status_code
    assert get_response_status == 200
    random_id = Book.objects.all().values_list("id", flat=True)[
        random.randint(0, (len(Book.objects.all()) - 1))
    ]
    get_response_data = client.get("/books/" + str(random_id) + "/").content.decode(
        "utf-8"
    )
    expected_data = json.dumps(
        {
            "id": random_id,
            "title": "Book",
            "published_date": "2006-03-28",
            "categories": [
                {"id": c1_pk, "name": "Category1"},
            ],
            "authors": [
                {"id": a1_pk, "name": "Author1"},
            ],
        },
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# 書籍の削除が出来ているかテスト
def test_delete_book_api(setup_book_object, client):
    b1_pk = Book.objects.get(title="Book1").pk
    delete_response_status = client.delete("/books/" + str(b1_pk) + "/").status_code
    assert delete_response_status == 204
    get_response_data = client.get("/books/").content.decode("utf-8")
    expected_data = json.dumps([])
    assert expected_data == get_response_data


# 単数著者をセットアップ
@pytest.fixture()
def setup_author_object():
    author = Author(name="Author1")
    author.save()


# ユニークな名前の著者を複数セットアップ
@pytest.fixture()
def setup_multiple_author_objects(request):
    for i in range(request.param):
        author = Author(name="Author" + str(i + 1))
        author.save()


# 複数の著者を一覧で取得出来ることをテスト(テストする著者数：5, 10, 50 100)
@pytest.mark.parametrize(
    "setup_multiple_author_objects", [5, 10, 50, 100], indirect=True
)
def test_get_author_list_detail_api(setup_multiple_author_objects, client):
    get_response = client.get("/authors/")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    author_amount = len(Author.objects.all())
    generate_expected_data = []
    for i in range(author_amount):
        x = {
            "id": Author.objects.get(name="Author" + str(i + 1)).pk,
            "name": "Author" + str(i + 1),
        }
        generate_expected_data.append(x)
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        generate_expected_data,
        separators=(",", ":"),
    )
    assert expected_data == response_data


# 単数著者の登録が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "name": "Author",
            },
            {
                "id": 1,
                "name": "Author",
            },
        ),
        (
            {
                "id": None,
                "name": "著者",
            },
            {
                "id": 2,
                "name": "著者",
            },
        ),
        (
            {
                "id": None,
                "name": "Mix半角全角",
            },
            {
                "id": 1,
                "name": "Mix半角全角",
            },
        ),
    ],
)
def test_post_author_detail_api(test_input, expected, client):
    post_response_status = client.post(
        "/authors/", data=json.dumps(test_input), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    expected["id"] = Author.objects.get(name=expected["name"]).pk
    expected_data = json.dumps([expected], separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/authors/").content.decode("utf-8")
    assert expected_data == get_response_data


# 単数著者の編集が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "name": "Updated Author",
            },
            {
                "id": 1,
                "name": "Updated Author",
            },
        ),
        (
            {
                "id": None,
                "name": "アップデート著者",
            },
            {
                "id": 2,
                "name": "アップデート著者",
            },
        ),
        (
            {
                "id": None,
                "name": "Updated半角全角Author",
            },
            {
                "id": 2,
                "name": "Updated半角全角Author",
            },
        ),
    ],
)
def test_put_author_detail_api(setup_author_object, test_input, expected, client):
    a1_pk = Author.objects.get(name="Author1").pk
    test_input["id"] = a1_pk
    put_response_status = client.put(
        "/authors/" + str(a1_pk) + "/",
        data=json.dumps(test_input),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    expected["id"] = a1_pk
    expected_data = json.dumps(expected, separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/authors/" + str(a1_pk) + "/").content.decode(
        "utf-8"
    )
    assert expected_data == get_response_data


# 複数著者から指定した著者が取得出来ることをテスト(テストする著者数：5, 10, 50 100)
@pytest.mark.parametrize(
    "setup_multiple_author_objects", [5, 10, 50, 100], indirect=True
)
def test_get_author_detail_api(setup_multiple_author_objects, client):
    response = client.get("/authors/")
    get_response_status = response.status_code
    assert get_response_status == 200
    random_id = Author.objects.all().values_list("id", flat=True)[
        random.randint(0, (len(Author.objects.all()) - 1))
    ]
    get_response_data = client.get("/authors/" + str(random_id) + "/").content.decode(
        "utf-8"
    )
    name = Author.objects.get(id=random_id)
    expected_data = json.dumps(
        {"id": random_id, "name": str(name)},
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# 著者の削除が出来ているかテスト
def test_delete_author_api(setup_author_object, client):
    a1_pk = Author.objects.get(name="Author1").pk
    delete_response_status = client.delete("/authors/" + str(a1_pk) + "/").status_code
    assert delete_response_status == 204
    get_response_data = client.get("/authors/").content.decode("utf-8")
    expected_data = json.dumps([])
    assert expected_data == get_response_data


# 単数カテゴリーをセットアップ
@pytest.fixture()
def setup_category_object():
    category = Category(name="Category1")
    category.save()


# ユニークな名前のカテゴリーを複数セットアップ
@pytest.fixture()
def setup_multiple_category_objects(request):
    for i in range(request.param):
        category = Category(name="Category" + str(i + 1))
        category.save()


# 複数のカテゴリーを一覧で取得出来ることをテスト(テストするカテゴリー数：5, 10, 50 100)
@pytest.mark.parametrize(
    "setup_multiple_category_objects", [5, 10, 50, 100], indirect=True
)
def test_get_category_list_detail_api(setup_multiple_category_objects, client):
    get_response = client.get("/categories/")
    get_response_status = get_response.status_code
    assert get_response_status == 200
    category_amount = len(Category.objects.all())
    generate_expected_data = []
    for i in range(category_amount):
        x = {
            "id": Category.objects.get(name="Category" + str(i + 1)).pk,
            "name": "Category" + str(i + 1),
        }
        generate_expected_data.append(x)
    response_data = get_response.content.decode("utf-8")
    expected_data = json.dumps(
        generate_expected_data,
        separators=(",", ":"),
    )
    assert expected_data == response_data


# 単数カテゴリーの登録が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "name": "Category",
            },
            {
                "id": 1,
                "name": "Category",
            },
        ),
        (
            {
                "id": None,
                "name": "カテゴリー",
            },
            {
                "id": 2,
                "name": "カテゴリー",
            },
        ),
        (
            {
                "id": None,
                "name": "Mix半角全角",
            },
            {
                "id": 1,
                "name": "Mix半角全角",
            },
        ),
    ],
)
def test_post_author_detail_api(test_input, expected, client):
    form_data = test_input
    post_response_status = client.post(
        "/categories/", data=json.dumps(form_data), content_type="application/json"
    ).status_code
    assert post_response_status == 201
    expected["id"] = Category.objects.get(name=expected["name"]).pk
    expected_data = json.dumps([expected], separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/categories/").content.decode("utf-8")
    assert expected_data == get_response_data


# 単数カテゴリーの編集が出来ることをテスト
# テストケース：半角のみ（英語）・全角のみ（日本語）・半角全角
@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {
                "id": None,
                "name": "Updated Category",
            },
            {
                "id": 1,
                "name": "Updated Category",
            },
        ),
        (
            {
                "id": None,
                "name": "アップデートカテゴリー",
            },
            {
                "id": 2,
                "name": "アップデートカテゴリー",
            },
        ),
        (
            {
                "id": None,
                "name": "Updated半角全角Category",
            },
            {
                "id": 2,
                "name": "Updated半角全角Category",
            },
        ),
    ],
)
def test_put_category_detail_api(setup_category_object, test_input, expected, client):
    c1_pk = Category.objects.get(name="Category1").pk
    test_input["id"] = c1_pk
    put_response_status = client.put(
        "/categories/" + str(c1_pk) + "/",
        data=json.dumps(test_input),
        content_type="application/json",
    ).status_code
    assert put_response_status == 200
    expected["id"] = c1_pk
    expected_data = json.dumps(expected, separators=(",", ":"), ensure_ascii=False)
    get_response_data = client.get("/categories/" + str(c1_pk) + "/").content.decode(
        "utf-8"
    )
    assert expected_data == get_response_data


# 複数カテゴリーから指定したカテゴリーが取得出来ることをテスト(テストするカテゴリー数：5, 10, 50 100)
@pytest.mark.parametrize(
    "setup_multiple_category_objects", [5, 10, 50, 100], indirect=True
)
def test_get_category_detail_api(setup_multiple_category_objects, client):
    response = client.get("/categories/")
    get_response_status = response.status_code
    assert get_response_status == 200
    random_id = Category.objects.all().values_list("id", flat=True)[
        random.randint(0, (len(Category.objects.all()) - 1))
    ]
    get_response_data = client.get(
        "/categories/" + str(random_id) + "/"
    ).content.decode("utf-8")
    name = Category.objects.get(id=random_id)
    expected_data = json.dumps(
        {"id": random_id, "name": str(name)},
        separators=(",", ":"),
    )
    assert expected_data == get_response_data


# カテゴリーの削除が出来ているかテスト
def test_delete_category_api(setup_category_object, client):
    c1_pk = Category.objects.get(name="Category1").pk
    delete_response_status = client.delete(
        "/categories/" + str(c1_pk) + "/"
    ).status_code
    assert delete_response_status == 204
    get_response_data = client.get("/categories/").content.decode("utf-8")
    expected_data = json.dumps([])
    assert expected_data == get_response_data
