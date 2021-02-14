from rest_framework.serializers import ModelSerializer

from .models import Book, Category, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "categories", "authors"]
