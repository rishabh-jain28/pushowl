# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class BookSerializer(serializers.ModelSerializer):
    last_borrower = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['owl_id', 'title', 'author', 'book_type', 'last_borrower', 'last_borrowed_date', 'borrowed_by', 'borrowed_date', 'return_date', 'available']
