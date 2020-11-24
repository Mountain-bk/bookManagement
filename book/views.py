from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def home_page(request):
    return render(request, 'book/index.html')
