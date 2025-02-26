from django.contrib import admin

from api.library.models import Book, BorrowRecord


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "stock", "publication_date"]
    list_filter = ["publication_date"]
    search_fields = ["title", "author"]


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "borrowed_at", "return_by", "returned_at", "is_overdue"]
    list_filter = ["borrowed_at"]
    search_fields = ["book__title", "user__email"]
