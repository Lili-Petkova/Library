from django.contrib import admin

from .models import Author, Book, Publisher, Store


class BookInLine(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [BookInLine]


@admin.register(Publisher)
class PublisherModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ['book__name']
    list_filter = ['book__author']


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    list_display = ["name", 'author', 'publisher']
    list_filter = ['author', 'store', 'publisher']
    search_fields = ['name']


@admin.register(Store)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    filter_horizontal = ['books']
    list_filter = ['books__author']
    actions_selection_counter = True
