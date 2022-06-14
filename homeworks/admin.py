from django.contrib import admin
from . import models


@admin.register(models.Homework)
class HomeworkAdmin(admin.ModelAdmin):

    list_display = (
        "study_class",
        "subject",
        "book",
        "homework_text",
        "video_url",
        "get_users_string",
        "get_wrong_answer_union",
    )

    list_filter = (
        "study_class",
        "subject",
        "book",
    )


@admin.register(models.WrongAnswer)
class WrongAnswersAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "homework",
        "wrong_answer_string",
    )

    list_filter = (
        "homework__study_class",
        "homework__subject",
        "homework__book",
    )
