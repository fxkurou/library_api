from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Book(models.Model):
    """
    Book model class.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        publication_date (date): The publication date of the book.
        stock (int): The stock of the book.
    """

    title = models.CharField(_("title"), max_length=255)
    author = models.CharField(_("author"), max_length=255)
    publication_date = models.DateField(_("publication date"))
    stock = models.PositiveIntegerField(_("stock"), default=0)

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ["-publication_date"]

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_by = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="borrowed_books",
        verbose_name=_("user"),
    )
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        related_name="borrowed_books",
        verbose_name=_("book"),
    )

    @property
    def is_overdue(self):
        return self.returned_at is None and self.return_by < now().date()
