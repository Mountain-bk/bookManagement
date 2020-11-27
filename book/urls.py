from django.urls import path
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('author/', views.author_view, name='author'),
    path('author-edit/<int:id>', views.author_edit_view, name='author edit'),
    path('author-register/', views.author_register_view, name='author register'),
    path('author-delete/<int:id>', views.author_delete_view, name='author delete'),
    path('category/', views.category_view, name='category'),
    path('category-edit/<int:id>', views.category_edit_view, name='category edit'),
    path('category-register/', views.category_register_view, name='category register'),
    path('category-delete/<int:id>', views.category_delete_view, name='category delete')
]
