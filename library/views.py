from django.db.models import Avg, Count
from django.shortcuts import render

from library.models import Author, Book, Publisher, Store


def start(request):
    return render(request, 'library/start.html')


def authors(request):
    all_authors = Author.objects.all().annotate(count_books=Count('book'))
    return render(
        request,
        'library/authors.html',
        {
            'all_authors': all_authors,
        }
    )


def one_author(request, name):
    author = Author.objects.get(name=name)
    book = Book.objects.prefetch_related("store_set").filter(author__name=author)
    life = author.date_of_death.year-author.date_of_birth.year

    return render(
        request,
        'library/one_author.html',
        {
            'author': author,
            'author_books': book,
            'life': life
        }
    )


def books(request):
    all_books = Book.objects.select_related('author').all()
    all_author = Author.objects.all()
    pr = round(Book.objects.aggregate(Avg('price'))['price__avg'])
    return render(
        request,
        'library/books.html',
        {
            'all_books': all_books,
            'all_author': all_author,
            'pr': pr
        }
    )


def one_book(request, name):
    book = Book.objects.get(name=name)
    all_book = Book.objects.filter(name=name).annotate(count_store=Count('store'))

    return render(
        request,
        'library/one_book.html',
        {
            'book': book,
            'all': all_book,
        }
    )


def publishers(request):
    all_publishers = Publisher.objects.all()

    return render(
        request,
        'library/publishers.html',
        {
            'all_publishers': all_publishers,
        }
    )


def one_publisher(request, pk):
    this_books = Book.objects.filter(publisher__id=pk)
    amount = this_books.count()
    return render(
        request,
        'library/one_publisher.html',
        {
            'this_books': this_books,
            'amount': amount
        }
    )


def stores(request):
    all_stores = Store.objects.all().annotate(count_books=Count('books'))
    return render(
        request,
        'library/stores.html',
        {
            'all_stores': all_stores,
        }
    )


def one_store(request, pk):
    store = Store.objects.prefetch_related('books').get(pk=pk)
    storebooks = store.books.all()
    price = round(Book.objects.filter(store__id=pk).aggregate(Avg('price'))['price__avg'])

    return render(
        request,
        'library/one_store.html',
        {
            'store': store,
            'storebooks': storebooks,
            'price': price,
        }
    )
