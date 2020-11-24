from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page),
    path('author/', views.author_view, name='author')
]
