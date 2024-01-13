# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AvailableBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)

class Book(models.Model):
    BOOK_TYPES = [
        ('Paperback', 'Paperback'),
        ('Hardcover', 'Hardcover'),
        ('Handmade', 'Handmade'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES)
    owl_id = models.AutoField(primary_key=True, unique=True)
    last_borrower = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='last_borrower')
    last_borrowed_date = models.DateField(null=True, blank=True)
    borrowed_by = models.CharField(max_length=255, null=True, blank=True)
    borrowed_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    available = models.BooleanField(default=True)

    objects = models.Manager()  # Default manager
    available_books = AvailableBookManager()  # Custom manager for available books

    def __str__(self):
        return f"{self.title} by {self.author}"
