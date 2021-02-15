import csv
import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rest_framework.viewsets import ModelViewSet

from .forms import AuthorForm, BookForm, CategoryForm
from .models import Author, Book, Category
from .serializers import AuthorSerializer, BookSerializer, CategorySerializer


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
    if request.method == "POST":
        if 'csv-export' in request.POST:
            response = HttpResponse(content_type="text/csv")
            today_string = datetime.datetime.today().strftime("%x")

            # ファイル名　'book_detail_01_16_21.csv'
            response[
                "Content-Disposition"
            ] = f'attachment; filename="book_detail_{today_string}.csv"'

            writer = csv.writer(response)
            # ヘッダー
            writer.writerow(
                ["No.", "Title", "Published Date", "Author", "Category"])
            for index, book in enumerate(
                Book.objects.all().prefetch_related("authors", "categories"), 1
            ):
                authors = ", ".join(
                    [author.name for author in book.authors.all()])
                categories = ", ".join(
                    [category.name for category in book.categories.all()])

                # ""で囲んで表示したい場合は f'"{authors}"'

                writer.writerow(
                    [index, book.title, book.published_date, authors, categories])
            return response
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


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
