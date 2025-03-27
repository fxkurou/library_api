from datetime import timedelta

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view

from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from api.library.models import Book, BorrowRecord
from api.library.serializers import BookSerializer, BorrowRecordSerializer
from api.library.tasks import send_email_notification


@extend_schema_view(
    post=extend_schema(
        tags=["library"],
        request=BookSerializer,
        responses={201: BookSerializer},
        description="Create a new book.",
        examples=[
            OpenApiExample(
                "Example request",
                value={
                    "title": "Book Title",
                    "slug": "Book Slug",
                    "author": "Book Author",
                    "publication_date": "2022-01-01",
                    "stock": 10,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example response",
                value={
                    "id": 1,
                    "title": "Book Title",
                    "slug": "Book Slug",
                    "author": "Book Author",
                    "publication_date": "2022-01-01",
                    "stock": 10,
                },
                response_only=True,
            ),
        ],
    ),
    get=extend_schema(
        tags=["library"],
        responses={200: BookSerializer(many=True)},
        description="List all books.",
        examples=[
            OpenApiExample(
                "Example response",
                value=[
                    {
                        "id": 1,
                        "title": "Book Title 1",
                        "slug": "Book Slug 1",
                        "author": "Book Author 1",
                        "publication_date": "2022-01-01",
                        "stock": 10,
                    },
                    {
                        "id": 2,
                        "title": "Book Title 2",
                        "slug": "Book Slug 2",
                        "author": "Book Author 2",
                        "publication_date": "2022-02-02",
                        "stock": 5,
                    },
                ],
                response_only=True,
            ),
        ],
    ),
)
class BookView(
    generics.ListCreateAPIView,
):
    """
    List all books or create a new book.

    To create a new book, send a POST request with the book title, author, and stock.
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()


@extend_schema_view(
    get=extend_schema(
        tags=["library"],
        responses={200: BookSerializer},
        description="Retrieve a book.",
        examples=[
            OpenApiExample(
                "Example response",
                value={
                    "id": 1,
                    "title": "Book Title",
                    "slug": "Book Slug",
                    "author": "Book Author",
                    "publication_date": "2022-01-01",
                    "stock": 10,
                },
                response_only=True,
            ),
        ],
    ),
    put=extend_schema(
        tags=["library"],
        request=BookSerializer,
        responses={200: BookSerializer},
        description="Update a book.",
        examples=[
            OpenApiExample(
                "Example request",
                value={
                    "title": "Book Title",
                    "slug": "Book Slug",
                    "author": "Book Author",
                    "publication_date": "2022-01-01",
                    "stock": 10,
                },
                request_only=True,
            ),
            OpenApiExample(
                "Example response",
                value={
                    "id": 1,
                    "title": "Book Title",
                    "slug": "Book Slug",
                    "author": "Book Author",
                    "publication_date": "2022-01-01",
                    "stock": 10,
                },
                response_only=True,
            ),
        ],
    ),
    delete=extend_schema(
        tags=["library"],
        responses={204: None},
        description="Delete a book.",
    ),
)
class BookDetailView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    """
    Retrieve, update, or delete a book.

    To update a book, send a PUT request with the book title, author, and stock.
    """

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, id=self.kwargs["pk"])

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        tags=["library"],
        request=BorrowRecordSerializer,
        responses={201: BorrowRecordSerializer},
        description="Borrow a book.",
        examples=[
            OpenApiExample(
                "Example request",
                value={"book": 1},
                request_only=True,
            ),
            OpenApiExample(
                "Example response",
                value={"id": 1, "user": 1, "book": 1, "return_by": "2022-01-01", "returned_at": None},
                response_only=True,
            ),
        ],
    ),
    get=extend_schema(
        tags=["library"],
        responses={200: BorrowRecordSerializer(many=True)},
        description="List all borrow records.",
        examples=[
            OpenApiExample(
                "Example response",
                value=[
                    {"id": 1, "user": 1, "book": 1, "return_by": "2022-01-01", "returned_at": None},
                    {"id": 2, "user": 1, "book": 2, "return_by": "2022-01-01", "returned_at": None},
                ],
                response_only=True,
            ),
        ],
    ),
)
class BorrowBookView(
    generics.ListCreateAPIView,
):
    """
    Borrow a book.

    To borrow a book, send a POST request with the book ID.
    """

    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRecord.objects.filter(returned_at__isnull=True)

    def create(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=request.data.get("book"))
        if book.stock <= 0:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        book.stock -= 1
        book.save()

        borrow_record = BorrowRecord.objects.create(
            user=request.user,
            book=book,
            return_by=now().date() + timedelta(days=14),
        )

        send_email_notification.delay(request.user.email, "Book Borrowed", f"You borrowed {book.title}")

        return Response(BorrowRecordSerializer(borrow_record).data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        tags=["library"],
        responses={200: BorrowRecordSerializer},
        description="Retrieve a borrow record.",
        examples=[
            OpenApiExample(
                "Example response",
                value={"id": 1, "user": 1, "book": 1, "return_by": "2022-01-01", "returned_at": None},
                response_only=True,
            ),
        ],
    ),
    patch=extend_schema(
        tags=["library"],
        request=BorrowRecordSerializer,
        responses={200: BorrowRecordSerializer},
        description="Return a book.",
        examples=[
            OpenApiExample(
                "Example response",
                value={"id": 1, "user": 1, "book": 1, "return_by": "2022-01-01", "returned_at": "2022-01-01T00:00:00Z"},
                response_only=True,
            ),
        ],
    ),
    delete=extend_schema(
        tags=["library"],
        responses={204: None},
        description="Delete a borrow record.",
    ),
)
class ReturnBookView(generics.RetrieveUpdateDestroyAPIView):
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


@extend_schema_view(
    get=extend_schema(
        tags=["library"],
        responses={200: BorrowRecordSerializer(many=True)},
        description="List all overdue books.",
        examples=[
            OpenApiExample(
                "Example response",
                value=[
                    {"id": 1, "user": 1, "book": 1, "return_by": "2022-01-01", "returned_at": None},
                    {"id": 2, "user": 1, "book": 2, "return_by": "2022-01-01", "returned_at": None},
                ],
                response_only=True,
            ),
        ],
    ),
)
class OverdueBooksView(generics.ListAPIView):
    """
    List all overdue books.

    To list all overdue books, send a GET request.
    """

    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BorrowRecord.objects.filter(
            user=self.request.user.id, returned_at__isnull=True, return_by__lt=now().date()
        )
