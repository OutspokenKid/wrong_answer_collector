from django.db import models
from core import models as core_models


class StudyClass(core_models.TimeStampedModel):
    """
    class_name : 반 이름, ex) 월수/수학1
    subject : 과목
    book : 교재
    """

    class_name = models.CharField(max_length=30, default="", null=True)
    subjects = models.ManyToManyField(
        "classes.Subject", related_name="classes", blank=True)
    books = models.ManyToManyField(
        "classes.Book", related_name="classes", blank=True)

    def __str__(self) -> str:
        return self.class_name

    def get_subjects_string(self):

        subjects_string = ""

        for subject in self.subjects.all():
            if subjects_string != "":
                subjects_string += ","

            subjects_string += subject.subject_name

        return subjects_string

    def get_books_string(self):

        books_string = ""

        for book in self.books.all():
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


class WrongAnswers(core_models.TimeStampedModel):
    """
    학생들의 오답 목록.

    user : 학생, foreign_key
    study_class : 반, foreign_key
    subject : 과목, foreign_key
    book : 교재, foreign_key
    wrong_answers : "1,2,3,4"와 같은 형식의 string
    """
    user = models.ForeignKey(
        "users.User", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        "classes.Subject", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(
        "classes.Book", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    wrong_answers = models.CharField(max_length=1000)


class Homework(core_models.TimeStampedModel):
    """
    숙제

    study_class : 어느 반의 숙제인지
    subejct : 어느 과목의 숙제인지
    book : 어느 교재의 숙제인지
    homework_text : 그날의 진도 또는 숙제
    user : 해당 숙제를 해야하는 유저.
    video_link : 유튜브 영상 있다면 추후에 추가.
    """

    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        "classes.Subject", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(
        "classes.Subject", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)

    homework_text = models.CharField(max_length=100)

    user = models.ManyToManyField(
        "users.User", related_name="homeworks", blank=True)
    video_link = models.CharField(max_length=100)
