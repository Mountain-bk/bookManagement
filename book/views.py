import csv
import datetime
from io import TextIOWrapper

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import AuthorForm, BookForm, CategoryForm
from .models import Author, Book, Category


# Create your views here.
def home_page(request):
    return render(request, "book/index.html")


def author_view(request):
    authors = Author.objects.all()
    return render(request, "book/author.html", {"authors": authors})


def author_edit_view(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Update submission succesfull")
            return redirect("book:author")
        else:
            messages.error(request, "Sorry, same author already exists")
            return redirect("book:author")
    else:
        form = AuthorForm(instance=author)
    return render(request, "book/author_edit.html", dict(form=form, id=id))


def author_register_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submission successful")
            return redirect("book:author")
        else:
            messages.error(request, "Sorry, same author already exists")
            return redirect("book:author")
    else:
        form = AuthorForm()
    return render(request, "book/author_register.html", {"form": form})


def author_delete_view(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.delete()
        messages.success(request, "Form submission successful")
        return redirect("book:author")
    return render(request, "book/author_delete.html", {"author": author})


def category_view(request):
    categories = Category.objects.all()
    return render(request, "book/category.html", {"categories": categories})


def category_edit_view(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Update submission succesfull")
            return redirect("book:category")
        else:
            messages.error(request, "Sorry, same category already exists")
            return redirect("book:category")
    else:
        form = CategoryForm(instance=category)
    return render(request, "book/category_edit.html", dict(form=form, id=id))


def category_register_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submission successful")
            return redirect("book:category")
        else:
            messages.error(request, "Sorry, same category already exists")
            return redirect("book:category")
    else:
        form = CategoryForm()
    return render(request, "book/category_register.html", {"form": form})


def category_delete_view(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Form submission successful")
        return redirect("book:category")
    return render(request, "book/category_delete.html", {"category": category})


def book_shelf_view(request):
    books = Book.objects.all()
    return render(request, "book/book_shelf.html", {"books": books})


def book_register_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form submission successful")
            return redirect("book:book shelf")
        else:
            messages.error(request, "Sorry, there is an error.")
            return redirect("book:book shelf")
    else:
        form = BookForm()
    return render(request, "book/book_register.html", {"form": form})


def book_edit_view(request, id):
    book = Book.objects.get(id=id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Update submission succesfull")
            return redirect("book:book shelf")
        else:
            messages.error(request, "Sorry, there is an error.")
            return redirect("book:book shelf")
    else:
        form = BookForm(instance=book)
    return render(request, "book/book_edit.html", dict(form=form, id=id))


def book_detail_view(request, id):
    book = Book.objects.get(id=id)
    return render(request, "book/book_detail.html", {"book": book})


def book_delete_view(request, id):
    book = Book.objects.get(id=id)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Form submission successful")
        return redirect("book:book shelf")
    return render(request, "book/book_delete.html", {"book": book})


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    today_string = datetime.datetime.today().strftime("%x")

    # ファイル名　'book_detail_01_16_21.csv'
    response[
        "Content-Disposition"
    ] = f'attachment; filename="book_detail_{today_string}.csv"'

    writer = csv.writer(response)
    # ヘッダー
    writer.writerow(["No.", "Title", "Published Date", "Author", "Category"])
    for index, book in enumerate(
        Book.objects.all().prefetch_related("authors", "categories"), 1
    ):
        authors = ", ".join([author.name for author in book.authors.all()])
        categories = ", ".join(
            [category.name for category in book.categories.all()])

        # ""で囲んで表示したい場合は f'"{authors}"'

        writer.writerow(
            [index, book.title, book.published_date, authors, categories])
    return response


def import_csv(request):
    # CSVファイルかの確認
    if not request.FILES['csv'].name.endswith('.csv'):
        messages.error(request, "Wrong File Format")
        return redirect("book:book shelf")
    form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
    csv_file = csv.reader(form_data)
    next(csv_file, None)
    duplicate_list = []
    error_list = []
    for line in csv_file:
        duplicate = False
        author_names = line[2].split(",")
        category_names = line[3].split(",")
        # タイトルと著者の完全一致が無いかの確認
        if Book.objects.filter(title=line[0]):
            same_books = list(Book.objects.filter(title=line[0]))
            for same_book in same_books:
                exist_authors = list(
                    same_book.authors.values_list('name', flat=True))
                if sorted(exist_authors) == sorted(author_names):
                    print("Error")
                    duplicate = True
                    duplicate_list.append(line[0])
                    break

        if duplicate:
            continue

        try:
            book = Book.objects.create(title=line[0], published_date=line[1])
            for category_name in category_names:
                category, _ = Category.objects.get_or_create(
                    name=category_name)
                book.categories.add(category)
            for author_name in author_names:
                author, _ = Author.objects.get_or_create(name=author_name)
                book.authors.add(author)
        except ValidationError as e:
            error_list.extend(e)

    if duplicate_list is not None:
        error_list.append(
            f"{duplicate_list} are not registered due to duplicate error")

    if error_list is not None:
        for error in error_list:
            messages.warning(request, error)
        return redirect("book:book shelf")
    else:
        messages.success(request, "Form submission successful")
        return redirect("book:book shelf")


def export_template(request):
    response = HttpResponse(content_type="text/csv")
    response[
        "Content-Disposition"
    ] = 'attachment; filename="book_upload_file.csv"'
    writer = csv.writer(response)
    writer.writerow(["Title(Required)", "Published Date('2021-01-30)",
                     "Author(Author1,Author2)", "Category(Category1,Category2)"])
    return response
