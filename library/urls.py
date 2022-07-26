from django.urls import path

from library.views import authors, books, one_author, one_book, one_publisher, one_store, publishers, start, stores


app_name = 'library'
urlpatterns = [
    path('', start, name='start'),
    path('authors/', authors, name='authors'),
    path('books/', books, name='books'),
    path('publishers/', publishers, name='publishers'),
    path('stores/', stores, name='stores'),
    path('stores/<int:pk>', one_store, name='one_store'),
    path('publishers/<int:pk>', one_publisher, name='one_publisher'),
    path('authors/<name>', one_author, name='one_author'),
    path('books/<name>', one_book, name='one_book'),
]
