from django.db import models
from core import models as core_models


class Homework(core_models.TimeStampedModel):
    """
    숙제

    study_class : 어느 반의 숙제인지
    subject : 어느 과목의 숙제인지
    book : 어느 교재의 숙제인지
    homework_text : 그날의 진도 또는 숙제
    video_url : 유튜브 영상 있다면 추후에 추가

    wrong_answer_union : 오답의 합집합
    """

    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        "classes.Subject", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(
        "classes.Book", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)

    users = models.ManyToManyField(
        "users.User", related_name="homeworks", blank=True)

    homework_text = models.CharField(max_length=100)
    video_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):

        return f"{self.study_class.class_name} - {self.subject.subject_name}, {self.book.book_name}, {self.homework_text}"

    def get_wrong_answer_union(self):

        wrong_answer_union = []

        for wrong_answer in self.wrong_answers.all():

            for answer in wrong_answer.wrong_answer_string.split(","):

                if int(answer) not in wrong_answer_union:
                    wrong_answer_union.append(int(answer))

        wrong_answer_union.sort()

        return wrong_answer_union

    def get_users_string(self):

        users_string = ""

        for user in self.users.all():

            if users_string != "":
                users_string += ", "

            users_string += user.username

        return users_string


class WrongAnswer(core_models.TimeStampedModel):
    """
    학생들의 오답 목록.

    user : 학생, foreign_key
    homework : 숙제, foreign_key
    wrong_answers : "1,2,3,4"와 같은 형식의 string
    """
    user = models.ForeignKey(
        "users.User", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    homework = models.ForeignKey(
        "homeworks.Homework", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    wrong_answer_string = models.CharField(max_length=1000)
