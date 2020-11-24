from django.shortcuts import render
from .models import Category
from .forms import CategoryForm

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
        form = CategoryForm(instance=category)
    return render(request, 'book/category_edit.html', dict(form=form, id=id))


