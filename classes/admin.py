from django.contrib import admin
from . import models


@admin.register(models.StudyClass)
class StudyClassAdmin(admin.ModelAdmin):

    list_display = (
        "class_name",
        "subject",
        "get_books_string",
        "get_users_count",
    )


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "subject_name",
    )


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        "book_name",
    )
