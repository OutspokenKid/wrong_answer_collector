from django.db import models
from core import models as core_models


class Student(core_models.TimeStampedModel):
    """
    username : email
    first_name : 이름
    last_name : 성

    class : 클래스 - foreign key
    """

    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)

    study_class = models.ForeignKey(
        "classes.Class", related_name="students", blank=True, null=True, on_delete=models.DO_NOTHING)
