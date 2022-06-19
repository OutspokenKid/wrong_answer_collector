from django.contrib import admin
from . import models


@admin.register(models.StudyClass)
class StudyClassAdmin(admin.ModelAdmin):

    list_display = (
        "class_name",
        "get_subjects_string",
        "get_books_string",
        "get_users_count",
    )


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "subject_name",
        "pk",
    )


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "book_name",
    )
