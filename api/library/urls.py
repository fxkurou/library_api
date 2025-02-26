from django.urls import path

from api.library.views import BookListCreateView, BorrowBookView, ReturnBookView, OverdueBooksView

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="books"),
    path("borrow/", BorrowBookView.as_view(), name="borrow"),
    path("return/<int:pk>/", ReturnBookView.as_view(), name="return"),
    path("overdue/", OverdueBooksView.as_view(), name="overdue"),
]
