from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"books", views.BookViewSet)
router.register(r"authors", views.AuthorViewSet)
router.register(r"categories", views.CategoryViewSet)

app_name = "book"
urlpatterns = [
    path("", include(router.urls)),
    path("home/", views.home_page, name="home"),
    path("author/", views.author_view, name="author"),
    path("author-edit/<int:id>", views.author_edit_view, name="author edit"),
    path("author-register/", views.author_register_view, name="author register"),
    path("author-delete/<int:id>", views.author_delete_view, name="author delete"),
    path("category/", views.category_view, name="category"),
    path("category-edit/<int:id>", views.category_edit_view, name="category edit"),
    path("category-register/", views.category_register_view, name="category register"),
    path(
        "category-delete/<int:id>", views.category_delete_view, name="category delete"
    ),
    path("book-shelf/", views.book_shelf_view, name="book shelf"),
    path("book-register/", views.book_register_view, name="book register"),
    path("book-edit/<int:id>", views.book_edit_view, name="book edit"),
    path("book-detail/<int:id>", views.book_detail_view, name="book detail"),
    path("book-delete/<int:id>", views.book_delete_view, name="book delete"),
]
