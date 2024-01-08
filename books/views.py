
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,BorrowedBook
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView,View,ListView
from profiles.models import UserProfile
from django.contrib import messages
from .forms import ReviewBookForm
from django.utils import timezone
from .constants import REVIEW_TYPE

class DetailBookView(DetailView):
      template_name='book_detail.html' 
      model=Book
      context_object_name='book'


@login_required(login_url='user_login')
def BorrowBookView(request, bookId):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=bookId)
        user_profile = get_object_or_404(UserProfile, user=request.user)

        if not book.is_available and user_profile.balance >= book.borrowing_price:
            
            BorrowedBook.objects.create(user=request.user, book=book)
            user_profile.balance -= book.borrowing_price
            user_profile.save()
            book.is_available=True
            book.save()
            messages.success(request, f'Book borrowed successfully.You Can add Review this Book. Your new balance is {user_profile.balance}')
            return redirect('detail_book',pk=bookId)
        elif  book.is_available:
            messages.error(request,'This book already borrowed !!')
        else:
            messages.error(request, 'Insufficient funds to borrow this book.')
    book = get_object_or_404(Book, pk=bookId)
    return render(request, 'book_detail.html', {'book': book})




class ProfilePageView(LoginRequiredMixin,ListView):
      template_name='user_profile.html'
      model=BorrowedBook
      context_object_name='books'
      login_url='user_login'

      def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.get_queryset()
        return context
      
@login_required(login_url='user_login')
def AddReviewView(request, bookId):
    book = get_object_or_404(Book, pk=bookId)
    
    if request.method == 'POST':
        if  book.is_available:
            review_form = ReviewBookForm(request.POST)
            if review_form.is_valid():
                book.user_reviews = review_form.cleaned_data['review']
                book.save()
                messages.success(request, 'Review added successfully.')
                return redirect('detail_book', pk=bookId)
        else:
            messages.error(request, 'please first Borrowing book before add  review.')
            review_form = ReviewBookForm(initial={'review': book.user_reviews})

            return render(request, 'book_detail.html', {'book': book, 'review_form': review_form})

    else:
        review_form = ReviewBookForm(initial={'review': book.user_reviews})

    return render(request, 'book_detail.html', {'book': book, 'review_form': review_form})

@login_required(login_url='user_login')
def ReturnBookView(request,bookId):

    if request.method=='POST':
        borrow_book = get_object_or_404(BorrowedBook, pk=bookId)
        if borrow_book.returned_date:
            messages.error(request, 'This book has already been returned.')
            return redirect('user_profile')
        else:
            borrow_book.returned_date=timezone.now()
            borrow_book.returned=True
            borrow_book.save()
            user_profile=UserProfile.objects.get(user=request.user)
            user_profile.balance += borrow_book.book.borrowing_price
            user_profile.save()
            borrow_book.book.is_available=False
            borrow_book.book.save()
            messages.success(request, f'Book returned successfully. Your new balance is {user_profile.balance}')
            return redirect('user_profile')