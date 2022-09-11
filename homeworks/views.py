from turtle import home
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from classes import models as class_models
from . import models


class HomeworkListView(View):

    def get(self, request):

        pks = []
        study_classes = []
        subjects = []
        books = []
        homework_texts = []
        created_ats = []
        is_wrong_answer_addeds = []

        homeworks = request.user.homeworks.all().order_by("-created_at")

        for homework in homeworks:

            pks.append(homework.pk)
            study_classes.append(homework.study_class)
            subjects.append(homework.subject)
            books.append(homework.book)
            homework_texts.append(homework.homework_text)
            created_ats.append(homework.created_at)
            is_wrong_answer_addeds.append(models.WrongAnswer.objects.filter(
                homework=homework, user=request.user).exists())

        zip_for_homework = zip(
            pks,
            study_classes,
            subjects,
            books,
            homework_texts,
            created_ats,
            is_wrong_answer_addeds,
        )

        return render(
            request,
            "homeworks/homework_list.html",
            {
                "zip_for_homework": zip_for_homework,
            },
        )


class HomeworkDetailView(View):

    def get(self, request, pk):

        homework = get_object_or_404(models.Homework, pk=pk)

        # 제출자, 미제출자 명단은 관리자에게만 노출.
        submitter = []
        unsubmitted = []

        if request.user.is_staff:

            wrong_answers = homework.wrong_answers.all()

            for wrong_answer in wrong_answers:
                submitter.append(wrong_answer.user)

            for user in homework.users.all():

                if user not in submitter:
                    unsubmitted.append(user)

        # 관리자는 오답 제출 안하고 입장 가능, 학생은 불가능.
        if not request.user.is_staff:
            my_wrong_answer = (request.user.wrong_answers.get(
                homework=homework)).wrong_answer_string.split(",")
        else:
            my_wrong_answer = None

        return render(
            request,
            "homeworks/homework_detail.html",
            {
                "homework": homework,
                "my_wrong_answer": my_wrong_answer,
                "submitter": submitter,
                "unsubmitted": unsubmitted,
            },
        )


class NewHomeworkView(View):

    def get(self, request):

        class_pk = request.GET.get("class_pk", -1)
        study_class = get_object_or_404(class_models.StudyClass, pk=class_pk)

        return render(
            request,
            "homeworks/new_homework.html",
            {
                "study_class": study_class,
            },
        )

    def post(self, request):

        selected_class_pk = request.POST.get("selected_class_pk", -1)
        selected_subject_pk = request.POST.get("selected_subject_pk", -1)
        selected_book_pk = request.POST.get("selected_book_pk", -1)
        homework_text = request.POST.get("homework_text", None)

        if selected_class_pk == -1 or selected_subject_pk == -1 or selected_book_pk == -1 or homework_text == "":

            return JsonResponse({
                "result": False,
                "message": "왜 빈거 보냄? 너 누구야",
            })

        study_class = class_models.StudyClass.objects.get(pk=selected_class_pk)
        subject = class_models.Subject.objects.get(pk=selected_subject_pk)
        book = class_models.Book.objects.get(pk=selected_book_pk)

        homework = models.Homework(
            study_class=study_class,
            subject=subject,
            book=book,
            homework_text=homework_text,
        )

        homework.save()

        return JsonResponse({
            "result": True,
            "message": "숙제 등록 완료",
        })


class CheckHomework(View):

    def get(self, request, pk):

        homeworks = models.Homework.objects.filter(study_class=pk)

        homework_pks = []
        homework_texts = []
        homework_checks = []

        for homework in homeworks:
            wrong_answers = models.WrongAnswer.objects.filter(
                homework=homework, user=request.user)

            homework_pks.append(homework.pk)
            homework_texts.append(
                homework.book.book_name + " - " + homework.homework_text)

            if wrong_answers:
                homework_checks.append(True)
            else:
                homework_checks.append(False)

        return JsonResponse({
            "result": True,
            "homework_pks": homework_pks,
            "homework_texts": homework_texts,
            "homework_checks": homework_checks,
        })


class WrongAnswerListView(View):

    def get(self, request):

        wrong_answers = models.WrongAnswer.objects.filter(
            user=request.user).order_by("-created_at")

        return render(
            request,
            "homeworks/wrong_answer_list.html",
            {
                "wrong_answers": wrong_answers,
            },
        )


class NewWrongAnswerView(View):

    def get(self, request, pk):

        homework = get_object_or_404(models.Homework, pk=pk)

        try:
            wrong_answer = models.WrongAnswer.objects.get(
                user=request.user, homework=homework)

            return render(
                request,
                "homeworks/new_wrong_answers.html",
                {
                    "homework": homework,
                    "homework_pk": pk,
                    "class_pk": homework.study_class.pk,
                    "wrong_answer_string": wrong_answer.wrong_answer_string,
                },
            )

        except models.WrongAnswer.DoesNotExist:

            return render(
                request,
                "homeworks/new_wrong_answers.html",
                {
                    "homework": homework,
                    "homework_pk": pk,
                    "class_pk": homework.study_class.pk,
                },
            )

    def post(self, request, pk):

        wrong_answers = request.POST.get("wrong_answers", "")
        homework = get_object_or_404(models.Homework, pk=pk)

        try:
            wrong_answer = models.WrongAnswer.objects.get(
                user=request.user, homework=homework)
            wrong_answer.wrong_answer_string = wrong_answers
            wrong_answer.save()
        except models.WrongAnswer.DoesNotExist:
            models.WrongAnswer.objects.create(
                user=request.user,
                homework=homework,
                wrong_answer_string=wrong_answers,
            )

        return JsonResponse({
            "result": True,
            "class_pk": homework.study_class.pk,
        })
