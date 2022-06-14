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

        # 유저 추가.
        users = study_class.users.all()
        user_json_objects = []

        for user in users:
            json_object = {
                "pk": user.pk,
                "username": user.username,
                "is_staff": user.is_staff,
            }

            user_json_objects.append(json_object)

        return JsonResponse({
            "result": True,
            "subject_objects": json.dumps(subject_json_objects),
            "book_objects": json.dumps(book_json_objects),
            "user_objects": json.dumps(user_json_objects),
        })
