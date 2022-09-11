from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    study_group : 클래스 - foreign key
    """

    study_group = models.ManyToManyField(
        "classes.StudyGroup", related_name="users", blank=True)

    def __str__(self):
        return self.username

    def get_study_groups(self):

        classes_string = ""

        for study_group in self.study_group.all():

            if classes_string != "":
                classes_string += ","

            classes_string += study_group.group_name

        return classes_string
