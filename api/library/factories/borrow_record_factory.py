import factory
from datetime import date, timedelta

from api.library.models import BorrowRecord


class BorrowRecordFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating BorrowRecord objects
    """

    class Meta:
        model = BorrowRecord

    user = factory.SubFactory("api.users.factories.UserFactory")
    book = factory.SubFactory("api.library.factories.BookFactory")
    borrowed_at = factory.LazyFunction(lambda: date.today())
    return_by = factory.LazyFunction(lambda: date.today() + timedelta(days=14))
    returned_at = factory.LazyFunction(lambda: date.today() + timedelta(days=7))
