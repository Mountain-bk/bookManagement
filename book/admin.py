from django.contrib import admin
from .models import Category, Book, Author

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'label_category', 'label_author')  # 一覧に出したい項目
    list_display_links = ('id', 'title', 'published_date', 'label_category', 'label_author')  # 修正リンクでクリックできる項目
    list_filter = ['categories__name', 'authors__name'] # カテゴリー、著者でフィルターをかける

    def label_category(self, obj):
        return " / ".join([category.name for category in obj.categories.all()]) # カテゴリーを1つずつ表示
    label_category.short_description = "Categories" # Indexのラベル指定

    def label_author(self, obj):
        return " / ".join([author.name for author in obj.authors.all()]) # 著者を1人ずつ表示
    label_author.short_description = "Authors" # Indexのラベル指定
    
admin.site.register(Book, BookAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)

admin.site.register(Category, CategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)

admin.site.register(Author, AuthorAdmin)


