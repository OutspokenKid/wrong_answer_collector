from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from classes import models as class_models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "is_staff",
        "get_study_classes",
    )

    fieldsets = (
        (None, {"fields": ("username", "is_staff", "study_class")},),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
