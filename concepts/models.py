from django.db import models
from core import models as core_models


class Concept(core_models.TimeStampedModel):
    """
    subject : 어떤 과목의 개념인지
    sequence_number : 몇 번째 개념인지
    title_text : 개념 이름
    pdf_url : 개념 프린트의 다운로드 링크
    pdf_teacher_url : 개념 프린트 교사용의 다운로드 링크
    video_url : 개념 영상의 링크
    """

    subject = models.ForeignKey(
        "classes.Subject", blank=True, null=True, on_delete=models.DO_NOTHING)
    sequence_number = models.IntegerField(default=0)
    title_text = models.CharField(max_length=20, blank=True, null=True)
    pdf_url = models.CharField(max_length=100, blank=True, null=True)
    pdf_teacher_url = models.CharField(max_length=100, blank=True, null=True)
    video_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.get_title_with_number()

    def get_title_with_number(self):

        return f"{self.sequence_number}. {self.title_text}"
