from django.shortcuts import render
from .models import Category

# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'book/category.html', {'categories': categories})

