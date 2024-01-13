from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Book, User
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import *

class BookListView(generics.ListCreateAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(available=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AuthorBookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        author_name = self.request.query_params.get('author')
        if author_name:
            return Book.objects.filter(author__iexact=author_name, borrowed_by=None)
        else:
            return Book.objects.none()

class BorrowBookView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        bookname = request.query_params.get('bookname')

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Find the book by name and author
        try:
            book = Book.objects.get(title__iexact=bookname)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the book is already borrowed
        if book.borrowed_by:
            return_date = book.return_date.strftime('%Y-%m-%d') if book.return_date else "unknown"
            return Response({
                "error": f"This book is already borrowed by another user. It will be available on {return_date}."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has borrowed the same book within the last 3 months
        if book.last_borrower == user and book.last_borrowed_date:
            if datetime.now().date() - book.last_borrowed_date < timedelta(days=90):
                return Response({"error": "You cannot borrow the same book within 3 months."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the author is popular (starts with 'J')
        if book.author.startswith('J'):
            six_months_ago = datetime.now().date() - timedelta(days=180)
            if Book.available_books.filter(last_borrower=user, author__startswith='J', last_borrowed_date__gte=six_months_ago).exists():
                return Response({"error": "You can only borrow one book from this popular author every 6 months."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate the return date
        return_date = datetime.now().date() + timedelta(days=14)

        # Update book details and mark it as borrowed
        book.last_borrower = user
        book.last_borrowed_date = datetime.now().date()
        book.borrowed_by = username
        book.borrowed_date = datetime.now().date()
        book.return_date = return_date
        book.available = False  # Set the book as unavailable
        book.save()

        return Response({"message": "Book successfully borrowed.", "return_date": return_date.strftime('%Y-%m-%d')}, status=status.HTTP_200_OK)



class ReturnBookView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        bookname = request.query_params.get('bookname')

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Find the book by name and author
        try:
            book = Book.objects.get(title__iexact=bookname, borrowed_by=user)
        except Book.DoesNotExist:
            return Response({"error": "Book not found or not borrowed by the specified user."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the book is ready to be returned
        if not book.borrowed_by or not book.return_date:
            return Response({"error": "Book is not currently borrowed or does not have a return date"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the return is overdue
        return_date = book.return_date
        today = datetime.now().date()

        if today > return_date:
            days_overdue = (today - return_date).days
            fine_amount = days_overdue * 5  # Assuming a fine of $5 per day overdue
            return Response({"error": f"Book is overdue by {days_overdue} days. Please pay a fine of ${fine_amount} to complete the return."}, status=status.HTTP_400_BAD_REQUEST)

        # Update book details and mark it as returned
        book.borrowed_by = None
        book.borrowed_date = None
        book.return_date = today
        book.available = True
        book.save()

        return Response({"message": "Book successfully returned."}, status=status.HTTP_200_OK)
