from django.urls import path
from .views import BookListView, AuthorBookListView, BorrowBookView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list-create'),
    path('author-books/', AuthorBookListView.as_view(), name='author-book-list'),
    path('borrow-book/', BorrowBookView.as_view(), name='borrow-book'),
    path('return-book/', ReturnBookView.as_view(), name='return-book'),
]
