from django.contrib import admin
from . import models


@admin.register(models.StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):

    list_display = (
        "group_name",
        "get_subjects_string",
        "get_books_string",
        "get_users_count",
    )


@admin.register(models.StudyClass)
class StudyClassAdmin(admin.ModelAdmin):

    list_display = (
        "study_group",
        "subject",
        "studied_at",
        "concept",
        "get_study_class_video_ids",
        "get_homework_video_ids",
    )

    list_filter = (
        "study_group",
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
