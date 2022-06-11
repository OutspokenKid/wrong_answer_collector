from django.contrib.auth.models import AbstractUser
from django.db import models
from core import models as core_models


class User(AbstractUser):
    """
    korean_name : 이름
    study_class : 클래스 - foreign key
    """

    korean_name = models.CharField(max_length=10, default="", null=True)
    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="users", blank=True, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.korean_name


class WrongAnswers(core_models.TimeStampedModel):
    """
    학생들의 오답 목록.

    user : 학생, foreign_key
    study_class : 반, foreign_key
    book : 교재, foreign_key
    wrong_answers : "1,2,3,4"와 같은 형식의 string
    """
    user = models.ForeignKey(
        "users.User", related_name="wrong_answers", blank=True, null=True, on_delete=models.DO_NOTHING)
    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="wrong_answers", blank=True, null=True, on_delete=models.DO_NOTHING)
    # book = models.ForeignKey(
    #     "classes.Book", related_name="wrong_answers", blank=True, null=True, on_delete=models.DO_NOTHING)
    wrong_answers = models.CharField(max_length=1000)
