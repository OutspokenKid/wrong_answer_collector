import json
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from . import models
from homeworks import models as homework_models


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

        zip_for_study_class_video = self.get_zip_for_study_class_video(
            study_class)

        zip_for_homework_video = self.get_zip_for_homework_video(study_class)

        get_zip_for_homework = self.get_zip_for_homework(
            request.user, study_class)

        return render(
            request,
            "classes/class_detail.html",
            {
                "study_class": study_class,
                "zip_for_study_class_video": zip_for_study_class_video,
                "zip_for_homework_video": zip_for_homework_video,
                "get_zip_for_homework": get_zip_for_homework,
            },
        )

    def get_zip_for_study_class_video(self, study_class):

        study_class_video_ids = study_class.get_study_class_video_ids()

        if study_class_video_ids:

            thumbnails = []
            urls = []

            for id in study_class_video_ids:
                thumbnails.append(
                    f"https://img.youtube.com/vi/{id}/maxresdefault.jpg")
                urls.append(f"https://www.youtube.com/watch?v={id}")

            return zip(thumbnails, urls)
        else:
            return None

    def get_zip_for_homework_video(self, study_class):

        homework_video_ids = study_class.get_homework_video_ids()

        if homework_video_ids:

            thumbnails = []
            urls = []

            for id in homework_video_ids:
                thumbnails.append(
                    f"https://img.youtube.com/vi/{id}/maxresdefault.jpg")
                urls.append(f"https://www.youtube.com/watch?v={id}")

            return zip(thumbnails, urls)
        else:
            return None

    def get_zip_for_homework(self, user, study_class):

        homeworks = homework_models.Homework.objects.filter(
            study_class=study_class)

        if homeworks:
            homeworks = []
            homework_texts = []
            homework_checks = []

            for homework in homeworks:

                homework.append(homework)
                homework_texts.append(
                    homework.book.book_name + " - " + homework.homework_text)

                wrong_answers = homework_models.WrongAnswer.objects.filter(
                    homework=homework, user=user)

                if wrong_answers:
                    homework_checks.append(True)
                else:
                    homework_checks.append(False)

            return zip(homeworks, homework_texts, homework_checks)
        else:
            return None


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
