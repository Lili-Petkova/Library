from django.urls import path

from library.views import authors, books, cities, one_author, one_book, one_publisher, one_store, publishers, start, stores

from . import views

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
    path('create_book/', views.BookCreateView.as_view(), name='create_book'),
    path('update_book/<int:pk>/', views.BookUpdateView.as_view(), name='update_book'),
    path('delete_book/<int:pk>/', views.BookDeleteView.as_view(), name='delete_book'),
    path('detail_book/<int:pk>/', views.BookDetailView.as_view(), name='detail_book'),
    path('all_books/', views.BookListView.as_view(), name='all_books'),
    path('cities/page/<int:page>/', cities, name="cities")
]
