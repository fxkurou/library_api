from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer
from datetime import timedelta
from django.utils.timezone import now
from .tasks import send_email_notification


class BookListCreateView(generics.ListCreateAPIView):
    """
    List all books or create a new book.

    To create a new book, send a POST request with the book title, author, and stock.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BorrowBookView(generics.CreateAPIView):
    """
    Borrow a book.

    To borrow a book, send a POST request with the book ID.
    """

    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=request.data.get("book"))
        if book.stock <= 0:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        book.stock -= 1
        book.save()

        borrow_record = BorrowRecord.objects.create(
            user=request.user,
            book=book,
            return_by=now().date() + timedelta(days=14),  # Default return period
        )

        # Asynchronous email notification
        send_email_notification.delay(request.user.email, "Book Borrowed", f"You borrowed {book.title}")

        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)


class ReturnBookView(generics.UpdateAPIView):
    """
    Return a book.

    To return a book, send a PATCH request with the borrow record ID.
    """

    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRecord.objects.filter(id=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        borrow_record = get_object_or_404(
            BorrowRecord, id=self.kwargs.get("pk"), user=request.user, returned_at__isnull=True
        )
        borrow_record.returned_at = now()
        borrow_record.book.stock += 1
        borrow_record.book.save()
        borrow_record.save()

        send_email_notification.delay(request.user.email, "Book Returned", f"You returned {borrow_record.book.title}")

        return Response(BorrowRecordSerializer(borrow_record).data)


class OverdueBooksView(generics.ListAPIView):
    """
    List all overdue books.

    To list all overdue books, send a GET request.
    """

    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRecord.objects.filter(user=self.request.user, returned_at__isnull=True, return_by__lt=now().date())
