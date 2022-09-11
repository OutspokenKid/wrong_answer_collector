from re import sub
from django.db import models
from core import models as core_models
import json

import homeworks


class Homework(core_models.TimeStampedModel):
    """
    숙제

    study_class : 어느 수업의 숙제인지
    subject : 어느 과목의 숙제인지
    book : 어느 교재의 숙제인지
    homework_text : 그날의 진도 또는 숙제

    wrong_answer_union : 오답의 합집합
    """

    study_class = models.ForeignKey(
        "classes.StudyClass", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        "classes.Subject", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(
        "classes.Book", related_name="homeworks", blank=True, null=True, on_delete=models.CASCADE)

    homework_text = models.CharField(max_length=100)

    def __str__(self):

        return f"{self.study_class.study_group.group_name} - {self.subject.subject_name}, {self.book.book_name}, {self.homework_text}"

    def get_study_group(self):

        return self.study_class.study_group

    def get_wrong_answer_union(self):

        wrong_answer_union = []

        for wrong_answer in self.wrong_answers.all():

            for answer in wrong_answer.wrong_answer_string.split(","):

                if int(answer) not in wrong_answer_union:
                    wrong_answer_union.append(int(answer))

        wrong_answer_union.sort()

        return wrong_answer_union

    def get_num_of_wrong_answer(self):

        return len(self.get_wrong_answer_union())

    def get_non_submit_users_string(self):

        usernames = []
        submit_usernames = []

        users = self.study_class.study_group.users.all()

        for user in users:
            usernames.append(user.username)

        usernames.remove("admin")

        wrong_answers = self.wrong_answers.all()

        for wrong_answer in wrong_answers:
            submit_username = wrong_answer.user.username

            if submit_username in usernames:
                submit_usernames.append(submit_username)

        complement = list(set(usernames) - set(submit_usernames))

        return complement


class WrongAnswer(core_models.TimeStampedModel):
    """
    학생들의 오답 목록.

    user : 학생, foreign_key
    homework : 숙제, foreign_key
    wrong_answer_string : "1,2,3,4"와 같은 형식의 string
    """
    user = models.ForeignKey(
        "users.User", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    homework = models.ForeignKey(
        "homeworks.Homework", related_name="wrong_answers", blank=True, null=True, on_delete=models.CASCADE)
    wrong_answer_string = models.CharField(max_length=1000)
