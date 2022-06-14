from django.contrib.auth.models import AbstractUser
from django.db import models
from core import models as core_models


class User(AbstractUser):
    """
    korean_name : 이름
    study_class : 클래스 - foreign key
    """

    study_class = models.ManyToManyField(
        "classes.StudyClass", related_name="users", blank=True)

    def __str__(self):
        return self.username

    def get_study_classes(self):

        classes_string = ""

        for study_class in self.study_class.all():

            if classes_string is not "":
                classes_string += ","

            classes_string += study_class.class_name

        return classes_string
