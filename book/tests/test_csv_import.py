import pytest
from book.models import Author, Book, Category
from django.core.files.uploadedfile import SimpleUploadedFile


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


# 入力形式が正しく、重複が無い場合に一括アップロードが成功することをテスト
def test_regular_csv_import(client):
    with open("testFiles/book_upload_file_regular_test.csv") as case1:
        import_file = SimpleUploadedFile(
            case1.name, bytes(case1.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == 'Form submission successful'
        expected_list = ['Title1', 'Title2', 'Title3']
        assert sorted(expected_list) == sorted(book_list)


# 必須入力項目に空欄が1つでもある場合にエラーを返し、全ての列がアップロードされないことをテスト
def test_blank_field_csv_import(client):
    with open("testFiles/book_upload_file_blank_field_test.csv") as case2:
        import_file = SimpleUploadedFile(
            case2.name, bytes(case2.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == 'Required field are not entered. Please fill required field'
        expected_list = []
        assert sorted(expected_list) == sorted(book_list)


# 日付の入力形式が1つでも違う場合にエラーを返し、全ての列がアップロードされないことをテスト
def test_wrong_date_format_csv_import(client):
    with open("testFiles/book_upload_file_wrong_date_format_test.csv") as case3:
        import_file = SimpleUploadedFile(
            case3.name, bytes(case3.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == 'Wrong date format. It must be in YYYY-MM-DD'
        expected_list = []
        assert sorted(expected_list) == sorted(book_list)


# タイトル＆著者が一致する書籍がデータベースに存在した場合にエラーを返し、全ての列がアップロードされないことをテスト
def test_db_duplicate_csv_import(setup_book_objects, client):
    with open("testFiles/book_upload_file_db_duplicate_test.csv") as case4:
        import_file = SimpleUploadedFile(
            case4.name, bytes(case4.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == "['星の王子様', '人間の大地'] have duplicate title and author"
        expected_list = ['星の王子様', '人間の大地']
        assert sorted(expected_list) == sorted(book_list)


# タイトル＆著者が一致する書籍がCSV内に存在した場合にエラーを返し、全ての列がアップロードされないことをテスト
def test_csv_duplicate_csv_import(client):
    with open("testFiles/book_upload_file_csv_duplicate_test.csv") as case5:
        import_file = SimpleUploadedFile(
            case5.name, bytes(case5.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == "['Title1'] have duplicate title and author"
        expected_list = []
        assert sorted(expected_list) == sorted(book_list)


# アップロードファイルがCSVではない場合にエラーを返すことをテスト
def test_wrong_file_format_import(client):
    with open("testFiles/book_upload_file_wrong_file_test.txt") as case6:
        import_file = SimpleUploadedFile(
            case6.name, bytes(case6.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list = []
        for book in books:
            book_list.append(book.title)
        response_message = messages[0]
        assert response_message.message == "Wrong File Format"
        expected_list = []
        assert sorted(expected_list) == sorted(book_list)


# エラーがあった場合に、エラーの種類のメッセージを全て表示し、全ての列がアップロードされないことをテスト
def test_multiple_error_csv_import(setup_book_objects, client):
    with open("testFiles/book_upload_file_multiple_error_test.csv") as case7:
        import_file = SimpleUploadedFile(
            case7.name, bytes(case7.read(), encoding='utf-8'))
        csv_data = {
            'csv-import': 'True',
            'csv': import_file
        }
        response = client.post(
            '/book-register/', csv_data, follow=True)
        messages = list(response.context['messages'])
        books = list(response.context['books'])
        book_list, error_list = [], []
        for book in books:
            book_list.append(book.title)
        for message in messages:
            print(message)
            error_list.append(message.message)
        expected_error_list = [
            "Required field are not entered. Please fill required field",
            "Wrong date format. It must be in YYYY-MM-DD",
            "['星の王子様'] have duplicate title and author"
        ]
        assert sorted(expected_error_list) == sorted(error_list)
        expected_book_list = ['星の王子様', '人間の大地']
        assert sorted(expected_book_list) == sorted(book_list)
