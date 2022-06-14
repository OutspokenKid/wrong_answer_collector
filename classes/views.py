import json
from statistics import mode
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from . import models


class ClassListView(View):

    def get(self, request):

        study_classes = models.StudyClass.objects.all()

        return render(
            request,
            "classes/class_list.html",
            {
                "study_classes": study_classes,
            },
        )


class ClassDetailView(View):

    def get(self, request, pk):

        study_class = get_object_or_404(models.StudyClass, pk=pk)

        return render(
            request,
            "classes/class_detail.html",
            {
                "study_classe": study_class,
            },
        )


class WrongAnswersListView(View):

    def get(self, request):

        wrong_answers = models.WrongAnswers.objects.filter(
            user=request.user).order_by("-created_at")

        return render(
            request,
            "classes/wrong_answer_list.html",
            {
                "wrong_answers": wrong_answers,
            },
        )


class ClassInfoView(View):

    def get(self, request, pk):

        book_pks = []
        book_names = []

        study_class = get_object_or_404(models.StudyClass, pk=pk)

        # 과목 추가.
        subjects = study_class.subjects.all()
        subject_json_objects = []

        for subject in subjects:
            json_object = {
                "pk": subject.pk,
                "subject_name": subject.subject_name
            }

            subject_json_objects.append(json_object)

        # 교재 추가.
        books = study_class.books.all()
        book_json_objects = []

        for book in books:
            json_object = {
                "pk": book.pk,
                "book_name": book.book_name
            }

            book_json_objects.append(json_object)

        return JsonResponse({
            "result": True,
            "books_pks": json.dumps(book_pks),
            "book_names": json.dumps(book_names),
            "subject_objects": json.dumps(subject_json_objects),
            "book_objects": json.dumps(book_json_objects),
        })


class NewWrongAnswersView(View):

    def get(self, request):

        # 내가 소속된 클래스 모두 가져옴.
        study_classes = request.user.study_class.all()

        return render(
            request,
            "classes/new_wrong_answers.html",
            {
                "study_classes": study_classes,
            },
        )

    def post(self, request):

        selected_class_pk = request.POST.get("selected_class_pk", -1)
        selected_subject_pk = request.POST.get("selected_subject_pk", -1)
        selected_book_pk = request.POST.get("selected_book_pk", -1)
        wrong_answers = request.POST.get("wrong_answers", "")

        if selected_class_pk == -1 or selected_subject_pk == -1 or selected_book_pk == -1 or not wrong_answers:

            return JsonResponse({
                "result": False,
                "message": "왜 빈거 보냄? 너 누구야",
            })

        study_class = models.StudyClass.objects.get(pk=selected_class_pk)
        subject = models.Subject.objects.get(pk=selected_subject_pk)
        book = models.Book.objects.get(pk=selected_book_pk)

        models.WrongAnswers.objects.create(
            user=request.user,
            study_class=study_class,
            subject=subject,
            book=book,
            wrong_answers=wrong_answers,
        )

        return JsonResponse({
            "result": True,
            "next": "",
        })
