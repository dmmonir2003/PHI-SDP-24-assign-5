

from django.urls import path
from .views import DetailBookView,ProfilePageView,BorrowBookView,AddReviewView,ReturnBookView
from core.views import CategoryBooksView
urlpatterns = [ 
    path('detail/<int:pk>/',DetailBookView.as_view(),name='detail_book'),
    path('user_profile/',ProfilePageView.as_view(),name='user_profile'),
    path('book_borrow/<int:bookId>/',BorrowBookView,name='book_borrow'),
    path('book_review/<int:bookId>/',AddReviewView,name='book_review'),
    path('book_return/<int:bookId>/',ReturnBookView,name='return_book'),
    path('category_books/<int:bookId>/',CategoryBooksView.as_view(),name='category_books'),
   
]
