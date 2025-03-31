import factory

from api.library.models import Book


class BookFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Book objects
    """

    class Meta:
        model = Book

    title = factory.Faker("sentence", nb_words=4)
    author = factory.Faker("name")
    slug = factory.Faker("slug")
    publication_date = factory.Faker("date")
    stock = factory.Faker("random_int", min=0, max=100)
