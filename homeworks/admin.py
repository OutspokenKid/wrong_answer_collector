from django.contrib import admin
from . import models


@admin.register(models.Homework)
class HomeworkAdmin(admin.ModelAdmin):

    list_display = (
        "study_class",
        "subject",
        "book",
        "homework_text",
        "get_non_submit_users_string",
        "get_wrong_answer_union",
        "get_num_of_wrong_answer",
    )

    list_filter = (
        "study_class__study_group",
        "subject",
        "book",
    )


@admin.register(models.WrongAnswer)
class WrongAnswersAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "homework",
        "created_at",
        "wrong_answer_string",
    )

    list_filter = (
        "homework__study_class",
        "homework__subject",
        "homework__book",
    )
