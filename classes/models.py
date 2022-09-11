from django.db import models
from core import models as core_models
import json


class StudyGroup(core_models.TimeStampedModel):
    """
    group_name : 반 이름, ex) 월수/수학1
    subject : 과목
    book : 교재
    """

    group_name = models.CharField(max_length=30, default="", null=True)
    subjects = models.ManyToManyField(
        "classes.Subject", related_name="groups", blank=True)
    books = models.ManyToManyField(
        "classes.Book", related_name="groups", blank=True)

    def __str__(self) -> str:
        return self.group_name

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


class StudyClass(core_models.TimeStampedModel):
    """
    그날 그날의 수업.

    study_group : 어느 반의 수업인지.
    subject : 어느 과목인지.
    studied_at : 수업한 날과 시간.
    concept : 그날 수업한 개념.
    study_class_video_ids : 그날 수업의 영상.
    homework_video_ids : 그날 수업의 영상.
    """

    def __str__(self) -> str:
        return f"{self.study_group} - {self.concept}"

    study_group = models.ForeignKey(
        "StudyGroup", related_name="classes", blank=True, null=True, on_delete=models.CASCADE)

    subject = models.ForeignKey(
        "classes.Subject", related_name="classes", null=True, on_delete=models.CASCADE)

    studied_at = models.DateTimeField(blank=True, null=True)

    concept = models.ForeignKey(
        "concepts.Concept", related_name="classes", blank=True, null=True, on_delete=models.CASCADE
    )

    study_class_video_ids = models.TextField(blank=True, null=True)
    homework_video_ids = models.TextField(blank=True, null=True)

    def save_study_class_video_ids(self, urls):

        if not urls or len(urls) == 0:
            return

        self.study_class_video_ids = json.dumps(urls)
        self.save()

    def get_study_class_video_ids(self):

        if self.study_class_video_ids:

            return json.decoder.JSONDecoder().decode(self.study_class_video_ids)

    def save_homework_video_ids(self, urls):

        if not urls or len(urls) == 0:
            return

        self.homework_video_ids = json.dumps(urls)
        self.save()

    def get_homework_video_ids(self):

        if self.homework_video_ids:

            return json.decoder.JSONDecoder().decode(self.homework_video_ids)


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
