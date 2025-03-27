from rest_framework import serializers
from .models import Book, BorrowRecord


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "slug",
            "publication_date",
            "stock",
        ]
        read_only_fields = [
            "id",
        ]


class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "book",
            "user",
            "borrowed_at",
            "returned_at",
            "return_by",
        ]
        read_only_fields = [
            "id",
        ]
