from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    pass
    # list_display = (
    #     "username",
    #     "first_name",
    #     "last_name",
    #     "study_class",
    # )

    # list_filter = (
    #     "study_class",
    # )


@admin.register(models.WrongAnswers)
class WrongAnswersAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "study_class",
        # "book",
    )
