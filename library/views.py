from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, Paginator
from django.db.models import Avg, Count
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.cache import cache_page

from library.forms import ContactForm
from library.models import Author, Book, City, Publisher, Store

from .tasks import send_mail


def start(request):
    return render(request, 'library/start.html')


def contact(request):
    data = dict()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            data['form_is_valid'] = True
            send_mail.delay(text, email)
            mes = messages.add_message(request,  messages.SUCCESS, 'Message sent')
            context = {'mes': mes}
            data['answer'] = render_to_string('library/includes/success.html', context, request=request)
        else:
            data['form_is_valid'] = False
    else:
        form = ContactForm()
    context = {'form': form}
    data['html_form'] = render_to_string('library/includes/contact_form.html', context, request=request)
    return JsonResponse(data)


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


@cache_page(60 * 30)
def cities(request):
    all_cities = City.objects.all().prefetch_related('store')
    page = request.GET.get('page', 1)
    paginator = Paginator(all_cities, 100)
    try:
        page_object = paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(
        request,
        'library/cities.html',
        {
            'paginator': paginator,
            'page': page_object,
        }
    )


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ["name", 'price', 'author', 'publisher', 'pubdate']
    success_url = reverse_lazy('library:books')
    login_url = '/admin/'


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    fields = ["name", 'price', 'author', 'publisher', 'pubdate']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('library:books')
    login_url = '/admin/'


class BookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Book
    template_name_suffix = '_check_delete'
    success_url = reverse_lazy('library:books')
    login_url = '/admin/'


class BookDetailView(generic.DetailView):
    model = Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    queryset = Book.objects.select_related("author")
