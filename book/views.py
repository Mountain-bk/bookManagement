from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm
from django.contrib import messages

# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')


def category_view(request):
    categories = Category.objects.all()
    return render(request, 'book/category.html', {'categories': categories})


def category_edit_view(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update submission succesfull')
            return redirect('book:category')
        else:
            messages.error(request, 'Sorry, same category already exists')
            return redirect('book:category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'book/category_edit.html', dict(form=form, id=id))


def category_register_view(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect('book:category')
        else:
            messages.error(request, 'Sorry, same category already exists')
            return redirect('book:category')
    else:
        form = CategoryForm()
    return render(request, 'book/category_register.html', {'form': form})


def category_delete_view(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Form submission successful')
        return redirect('book:category')
    return render(request, 'book/category_delete.html', {'category': category})
