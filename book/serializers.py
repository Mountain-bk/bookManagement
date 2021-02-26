from rest_framework.serializers import ModelSerializer

from .models import Book, Category, Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
        extra_kwargs = {
            "name": {"validators": []},
        }


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            "name": {"validators": []},
        }


class BookSerializer(ModelSerializer):
    authors = AuthorSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_date", "categories", "authors"]

    def create(self, validated_data):
        categories = validated_data.pop("categories", [])
        authors = validated_data.pop("authors", [])
        book = Book.objects.create(**validated_data)
        book.save()
        for category_name in categories:
            category, _ = Category.objects.get_or_create(name=category_name["name"])
            book.categories.add(category)
        for author_name in authors:
            author, _ = Author.objects.get_or_create(name=author_name["name"])
            book.authors.add(author)
        return book

    def update(self, instance, validated_data):
        print(instance)
        categories = validated_data.pop("categories", [])
        authors = validated_data.pop("authors", [])
        for item in validated_data:
            print(item)
            if Book._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.categories.clear()
        instance.authors.clear()
        for category_name in categories:
            category, _ = Category.objects.update_or_create(name=category_name["name"])
            instance.categories.add(category)
        for author_name in authors:
            author, _ = Author.objects.update_or_create(name=author_name["name"])
            instance.authors.add(author)
        instance.save()
        return instance
