from datetime import date

from django.test import tag
from rest_framework.test import APITestCase

from api.library.factories.borrow_record_factory import BorrowRecordFactory
from api.library.factories.book_factory import BookFactory


@tag("models")
class LibraryModelsTestCase(APITestCase):
    def test_book_model_successful(self):
        book = BookFactory(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            slug="the-great-gatsby",
            publication_date="1925-04-10",
            stock=10,
        )
        self.assertEqual(book.title, "The Great Gatsby")
        self.assertEqual(book.author, "F. Scott Fitzgerald")
        self.assertEqual(book.slug, "the-great-gatsby")
        self.assertEqual(book.publication_date, "1925-04-10")
        self.assertEqual(book.stock, 10)
        self.assertEqual(book.__str__(), "The Great Gatsby")

    def test_borrow_record_model_successful(self):
        borrow_record = BorrowRecordFactory()
        self.assertEqual(borrow_record.borrowed_at.date(), date(2025, 3, 31))
        self.assertEqual(borrow_record.return_by, date(2025, 4, 14))
        self.assertEqual(borrow_record.returned_at, date(2025, 4, 7))
        self.assertEqual(borrow_record.is_overdue, False)
