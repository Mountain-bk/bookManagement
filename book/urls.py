from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page),
    path('category/', views.category_view, name='category'),
    path('category-edit/<int:id>', views.category_edit_view, name='category edit')
]
