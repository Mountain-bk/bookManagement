from django.shortcuts import render, redirect
from .models import Author
from django.contrib import messages
from .forms import AuthorForm

# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')


def author_view(request):
    authors = Author.objects.all()
    return render(request, 'book/author.html', {'authors': authors})


def author_edit_view(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update submission succesfull')
            return redirect('book:author')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'book/author_edit.html', dict(form=form, id=id))


def author_register_view(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect('book:author')
    else:
        form = AuthorForm()
    return render(request, 'book/author_register.html', {'form': form})


def author_delete_view(request, id):
    author = Author.objects.get(id=id)
    if request.method == 'POST':
        author.delete()
        messages.success(request, 'Form submission successful')
        return redirect('book:author')
    return render(request, 'book/author_delete.html', {'author': author})
