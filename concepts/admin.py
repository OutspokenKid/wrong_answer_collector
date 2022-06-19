from django.contrib import admin
from . import models


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "get_title_with_number",
        "pdf_url",
        "video_url",
    )

    list_filter = (
        "subject",
    )
