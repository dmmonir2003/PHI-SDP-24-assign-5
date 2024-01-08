from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book,Categories

class BookListView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Categories.objects.all()
        return context

class CategoryBooksView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'

    def get_queryset(self):
        category_id = self.kwargs['bookId']
        return Book.objects.filter(category=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Categories.objects.all()
        return context