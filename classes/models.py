from django.db import models
from core import models as core_models


class Class(core_models.TimeStampedModel):
    """
    class_name
    grade
    """

    class_name = models.CharField(max_length=30, default="", null=True)
    grade = models.IntegerField(default=0)
