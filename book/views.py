from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Book, Category, Author
from .forms import BookForm, CategoryForm, AuthorForm
from django.contrib import messages


# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book:mypage')
    else:
        form = AuthenticationForm()
    return render(request, 'book/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book:mypage')
    else:
        form = UserCreationForm()
    return render(request, 'book/signup.html', {'form': form})


def logout_action(request):
    logout(request)
    return redirect('book:home')


def mypage_view(request):
    if request.user.is_authenticated:
        return render(request, 'book/mypage.html')
    else:
        return redirect('book:login')


def book_shelf_view(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    authors = Author.objects.all()
    title_contains_book = request.GET.get('title_contains')
    category = request.GET.get('category')
    author = request.GET.get('author')
    if title_contains_book != '' and title_contains_book is not None:
        books = books.filter(title__icontains=title_contains_book)
    if category != '' and category is not None and category != 'Choose...':
        books = books.filter(categories__name=category)
    if author != '' and author is not None and author != 'Choose...':
        books = books.filter(authors__name=author)
    context = {
        'books': books,
        'categories': categories,
        'authors': authors
    }
    return render(request, 'book/book_shelf.html', context)


def book_register_view(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect('book:book register')
    else:
        form = BookForm()
    return render(request, 'book/book_register.html', {'form': form})


def book_edit_view(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update submission succesfull')
            return redirect('book:book detail', id=id)
    else:
        form = BookForm(instance=book)
    return render(request, 'book/book_edit.html', dict(form=form, id=id))


def book_detail_view(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book/book_detail.html', {'book': book})


def book_delete_view(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Form submission successful')
        return redirect('book:bookshelf')
    return render(request, 'book/book_delete.html', {'book': book})


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'book/category.html', {'categories': categories})
