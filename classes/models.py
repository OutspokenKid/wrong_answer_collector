from django.db import models
from core import models as core_models


class StudyClass(core_models.TimeStampedModel):
    """
    class_name : 반 이름, ex) 월수/수학1
    subject : 과목
    book : 교재
    """

    class_name = models.CharField(max_length=30, default="", null=True)
    subject = models.ForeignKey(
        "classes.Subject", related_name="books", blank=True, null=True, on_delete=models.DO_NOTHING)
    book = models.ManyToManyField(
        "classes.Book", related_name="classes", blank=True, null=True)

    def __str__(self) -> str:
        return self.class_name

    def get_books_string(self):

        print(self.book.all())
        books_string = ""

        for book in self.book.all():
            if books_string != "":
                books_string += ","

            books_string += book.book_name

        return books_string

    def get_users_count(self):

        return self.users.count()


class Subject(core_models.TimeStampedModel):
    """
    subject_name : 과목 이름, ex) 수학1
    """

    subject_name = models.CharField(max_length=10, default="", null=True)

    def __str__(self):
        return self.subject_name


class Book(core_models.TimeStampedModel):
    """
    book_name : 책 이름, ex) 라이트쎈 수학1
    """

    book_name = models.CharField(max_length=20, default="", null=True)

    def __str__(self):
        return self.book_name
