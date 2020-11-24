from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page),
    path('author/', views.author_view, name='author'),
    path('author-edit/<int:id>', views.author_edit_view, name='author edit'),
    path('author-register/', views.author_register_view, name='author register')
]
