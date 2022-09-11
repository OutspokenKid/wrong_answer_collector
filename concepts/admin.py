from django.contrib import admin
from . import models


@admin.register(models.Concept)
class ConceptAdmin(admin.ModelAdmin):

    list_display = (
        "subject",
        "get_title_with_number",
        "pdf_url",
        "get_concept_video_ids",
    )

    list_filter = (
        "subject",
    )
