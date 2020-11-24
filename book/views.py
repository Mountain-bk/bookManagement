from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Book, Category, Author


# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')
