import json
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from . import models


class ClassListView(View):

    def get(self, request):

        study_classes = []

        study_groups = request.user.study_group.all()
        for study_group in study_groups:
            classes = list(study_group.classes.all())
            study_classes += classes

        study_classes = sorted(
            study_classes, key=lambda x: x.studied_at, reverse=True)

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

        study_class_video_ids = study_class.get_study_class_video_ids()
        zip_for_study_class_video = None

        if study_class_video_ids:

            thumbnails = []
            urls = []

            for id in study_class_video_ids:
                thumbnails.append(
                    f"https://img.youtube.com/vi/{id}/maxresdefault.jpg")
                urls.append(f"https://www.youtube.com/watch?v={id}")

            zip_for_study_class_video = zip(
                thumbnails,
                urls,
            )

        homework_video_ids = study_class.get_homework_video_ids()
        zip_for_homework_video = None

        if homework_video_ids:

            thumbnails = []
            urls = []

            for id in homework_video_ids:
                thumbnails.append(
                    f"https://img.youtube.com/vi/{id}/maxresdefault.jpg")
                urls.append(f"https://www.youtube.com/watch?v={id}")

            zip_for_homework_video = zip(
                thumbnails,
                urls,
            )

        return render(
            request,
            "classes/class_detail.html",
            {
                "study_class": study_class,
                "zip_for_study_class_video": zip_for_study_class_video,
                "zip_for_homework_video": zip_for_homework_video,
            },
        )


class ClassInfoView(View):

    def get(self, request, pk):

        book_pks = []
        book_names = []

        study_group = get_object_or_404(models.StudyGroup, pk=pk)

        # 과목 추가.
        subjects = study_group.subjects.all()
        subject_json_objects = []

        for subject in subjects:
            json_object = {
                "pk": subject.pk,
                "subject_name": subject.subject_name
            }

            subject_json_objects.append(json_object)

        # 교재 추가.
        books = study_group.books.all()
        book_json_objects = []

        for book in books:
            json_object = {
                "pk": book.pk,
                "book_name": book.book_name
            }

            book_json_objects.append(json_object)

        # 유저 추가.
        users = study_group.users.all()
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


class GroupListView(View):

    def get(self, request):

        study_groups = models.StudyGroup.objects.all()

        return render(
            request,
            "classes/group_list.html",
            {
                "study_groups": study_groups,
            },
        )
