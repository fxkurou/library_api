import factory

from api.library.factories.borrow_record_factory import BorrowRecordFactory
from api.library.factories.book_factory import BookFactory
from api.users.factories.user_factory import UserFactory


class BorrowRecordWithBookUserFactory(BorrowRecordFactory):
    """
    Factory for creating BorrowRecord objects with Book and User
    """

    book = factory.RelatedFactory(BookFactory, "book_fk")
    user = factory.RelatedFactory(UserFactory, "user_fk")
