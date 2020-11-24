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
