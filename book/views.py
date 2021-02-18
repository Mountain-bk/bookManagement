import csv
import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
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
        categories = ", ".join([category.name for category in book.categories.all()])

        # ""で囲んで表示したい場合は f'"{authors}"'

        writer.writerow([index, book.title, book.published_date, authors, categories])
    return response


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view(["GET", "POST", "DELETE"])
def book_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == "GET":
        books = Book.objects.all()

        title = request.GET.get("title", None)
        if title is not None:
            books = books.filter(title__icontains=title)

        books_serializer = BookSerializer(books, many=True)
        return JsonResponse(books_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == "POST":
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        count = Book.objects.all().delete()
        return JsonResponse(
            {"message": "{} Books were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def book_detail(request, id):
    # find tutorial by pk (id)
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse(
            {"message": "The book does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        book_serializer = BookSerializer(book)
        return JsonResponse(book_serializer.data)
    elif request.method == "PUT":
        book_data = JSONParser().parse(request)
        book_serializer = BookSerializer(book, data=book_data)
        if book_serializer.is_valid():
            book_serializer.save()
            return JsonResponse(book_serializer.data)
        return JsonResponse(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        book.delete()
        return JsonResponse(
            {"message": "Book was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "POST", "DELETE"])
def author_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == "GET":
        authors = Author.objects.all()

        name = request.GET.get("name", None)
        if name is not None:
            authors = authors.filter(name__icontains=name)

        authors_serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(authors_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == "POST":
        author_data = JSONParser().parse(request)
        author_serializer = AuthorSerializer(data=author_data)
        if author_serializer.is_valid():
            author_serializer.save()
            return JsonResponse(author_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(
            author_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        count = Author.objects.all().delete()
        return JsonResponse(
            {"message": "{} Authors were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def author_detail(request, id):
    # find tutorial by pk (id)
    try:
        author = Author.objects.get(id=id)
    except Author.DoesNotExist:
        return JsonResponse(
            {"message": "The author does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        author_serializer = AuthorSerializer(author)
        return JsonResponse(author_serializer.data)
    elif request.method == "PUT":
        author_data = JSONParser().parse(request)
        author_serializer = AuthorSerializer(author, data=author_data)
        if author_serializer.is_valid():
            author_serializer.save()
            return JsonResponse(author_serializer.data)
        return JsonResponse(
            author_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        author.delete()
        return JsonResponse(
            {"message": "Author was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "POST", "DELETE"])
def category_list(request):
    # GET list of tutorials, POST a new tutorial, DELETE all tutorials
    if request.method == "GET":
        categories = Category.objects.all()

        name = request.GET.get("name", None)
        if name is not None:
            categories = categories.filter(name__icontains=name)

        categories_serializer = CategorySerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == "POST":
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(
                category_serializer.data, status=status.HTTP_201_CREATED
            )
        return JsonResponse(
            category_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        count = Category.objects.all().delete()
        return JsonResponse(
            {"message": "{} Categories were deleted successfully!".format(count[0])},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view(["GET", "PUT", "DELETE"])
def category_detail(request, id):
    # find tutorial by pk (id)
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return JsonResponse(
            {"message": "The category does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    if request.method == "GET":
        category_serializer = CategorySerializer(category)
        return JsonResponse(category_serializer.data)
    elif request.method == "PUT":
        category_data = JSONParser().parse(request)
        category_serializer = CategorySerializer(category, data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse(category_serializer.data)
        return JsonResponse(
            category_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        category.delete()
        return JsonResponse(
            {"message": "Category was deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )
