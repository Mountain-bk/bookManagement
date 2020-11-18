from django.contrib import admin
from .models import Category, Book, Author

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'published_date', 'get_categories', 'get_authors')  # 一覧に出したい項目
    list_display_links = ('id', 'title', 'published_date', 'get_categories', 'get_authors')  # 修正リンクでクリックできる項目
    list_filter = ['categories', 'authors'] # カテゴリー、著者でフィルターをかける

    def get_categories(self, obj):  # 所属カテゴリーを取得
        return " / ".join([categories.name for categories in obj.categories.all()])

    def get_authors(self, obj):  # 著者を取得
        return " / ".join([author.name for author in obj.authors.all()])
    
admin.site.register(Book, BookAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)

admin.site.register(Category, CategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)

admin.site.register(Author, AuthorAdmin)


