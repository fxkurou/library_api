from django.urls import path

from api.library.views import (
    BookView,
    BorrowBookView,
    ReturnBookView,
    OverdueBooksView,
    BookDetailView,
)

urlpatterns = [
    path("books/", BookView.as_view(), name="books"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book"),
    path("borrow/", BorrowBookView.as_view(), name="borrow"),
    path("return/<int:pk>/", ReturnBookView.as_view(), name="return"),
    path("overdue/", OverdueBooksView.as_view(), name="overdue"),
]
