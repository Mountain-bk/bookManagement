from django.shortcuts import render
from .models import Author
from django.contrib import messages

# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')


def author_view(request):
    authors = Author.objects.all()
    return render(request, 'book/author.html', {'authors': authors})
