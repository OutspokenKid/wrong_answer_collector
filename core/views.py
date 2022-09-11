import datetime
import time
import xlrd
import xlwt
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from classes import models as class_models
from concepts import models as concept_models
from homeworks import models as homework_models
from users import models as user_models


class MainView(View):

    def get(self, request):

        return render(request, "main.html", {})


class AdminMenuView(View):

    def get(self, request):

        return render(request, "admin_menu.html", {})


class ExtractInformation(View):

    def get(self, request):

        class_objects = [
            # classes
            class_models.Subject,
            class_models.Book,
            class_models.StudyGroup,
            class_models.StudyClass,

            # concepts
            concept_models.Concept,

            # homeworks
            homework_models.Homework,
            homework_models.WrongAnswer,

            # users
            user_models.User,
        ]

        wb = xlwt.Workbook()

        for class_object in class_objects:
            self.save_objects_to_excel(wb, class_object)

        path = "assets/class_information.xls"
        wb.save(path)

        return JsonResponse({
            "result": True,
        })

    def save_objects_to_excel(self, wb, class_for_save):

        class_name = str(class_for_save).split("\'")[1].split(".")[-1]
        ws = wb.add_sheet(class_name)
        keys = list(class_for_save.objects.values()[0].keys())
        class_dicts = class_for_save.objects.values()

        for row_index in range(len(class_dicts) + 1):

            if row_index == 0:

                for key_index in range(len(keys)):
                    ws.write(row_index, key_index, keys[key_index])
            else:
                for column_index in range(len(keys)):

                    key = keys[column_index]
                    value = class_dicts[row_index-1][keys[column_index]]

                    # print(f"{key} : {value} ({type(value)})")

                    if isinstance(value, datetime.datetime):
                        timestamp = time.mktime(value.timetuple())
                        value = timestamp

                    ws.write(row_index, column_index, value)


class LoadInformation(View):

    def get(self, request):

        FILE_PATH = "assets/class_information.xls"

        # try:
        sheet_names = [
            'Subject',
            'Book',
            'StudyGroup',
            'StudyClass',
            'Concept',
            'Homework',
            'WrongAnswer',
            'User'
        ]

        # wb = xlrd.open_workbook(FILE_PATH)
        # self.save_user_models(wb.sheet_by_name(sheet_names[7]))
        # self.save_subject_models(wb.sheet_by_name(sheet_names[0]))
        # self.save_book_models(wb.sheet_by_name(sheet_names[1]))
        # self.save_concept_models(wb.sheet_by_name(sheet_names[4]))
        # self.save_study_group_models(wb.sheet_by_name(sheet_names[2]))
        # self.save_study_class_models(wb.sheet_by_name(sheet_names[3]))
        # self.save_homework_models(wb.sheet_by_name(sheet_names[5]))
        # self.save_wronganswer_models(wb.sheet_by_name(sheet_names[6]))

        return JsonResponse({
            "result": True,
        })

    def save_user_models(self, ws):

        users = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            user = user_models.User()
            user.pk = int(values[0])
            user.password = values[1]
            user.last_login = datetime.datetime.fromtimestamp(
                int(values[2]))
            user.is_superuser = values[3]
            user.username = values[4]
            user.is_staff = values[8]
            user.is_active = values[9]
            user.date_joined = datetime.datetime.fromtimestamp(
                int(values[10]))
            users.append(user)

        user_models.User.objects.bulk_create(users, ignore_conflicts=True)

    def save_book_models(self, ws):

        book_models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            book = class_models.Book()
            book.pk = int(values[0])
            book.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            book.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            book.book_name = values[3]

            book_models.append(book)

        class_models.Book.objects.bulk_create(book_models)

    def save_subject_models(self, ws):

        try:
            subject_models = []

            for i in range(ws.nrows):

                if i == 0:
                    continue

                # i번째 모델의 값 리스트.
                values = ws.row_values(i, 0)

                subject = class_models.Subject()
                subject.pk = int(values[0])
                subject.created_at = datetime.datetime.fromtimestamp(
                    int(values[1]))
                subject.updated_at = datetime.datetime.fromtimestamp(
                    int(values[2]))
                subject.subject_name = values[3]

                subject_models.append(subject)

            class_models.Subject.objects.bulk_create(subject_models)
        except:
            print("#########################")
            print("save_subject_models Error")
            print("#########################")

    def save_concept_models(self, ws):

        models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            model = concept_models.Concept()
            model.pk = int(values[0])
            model.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            model.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            model.subject = class_models.Subject.objects.get(pk=int(values[3]))
            model.sequence_number = values[4]
            model.title_text = values[5]
            model.pdf_url = values[6]
            model.pdf_teacher_url = values[7]
            model.concept_video_ids = values[8]

            models.append(model)

        concept_models.Concept.objects.bulk_create(models)

    def save_study_group_models(self, ws):

        models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            model = class_models.StudyGroup()
            model.pk = int(values[0])
            model.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            model.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            model.group_name = values[3]

            models.append(model)

        class_models.StudyGroup.objects.bulk_create(models)

    def save_study_class_models(self, ws):

        models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            model = class_models.StudyClass()
            model.pk = int(values[0])
            model.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            model.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            model.study_group = class_models.StudyGroup.objects.get(
                pk=values[3])
            model.subject = class_models.Subject.objects.get(pk=values[4])
            model.studied_at = datetime.datetime.fromtimestamp(
                int(values[5]))
            model.concept = concept_models.Concept.objects.get(pk=values[6])
            model.study_class_video_ids = values[7]
            model.homework_video_ids = values[8]

            models.append(model)

        class_models.StudyClass.objects.bulk_create(models)

    def save_homework_models(self, ws):

        models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            model = homework_models.Homework()
            model.pk = int(values[0])
            model.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            model.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            model.study_class = class_models.StudyClass.objects.get(
                pk=values[3])
            model.subject = class_models.Subject.objects.get(pk=values[4])
            model.book = class_models.Book.objects.get(pk=values[5])
            model.homework_text = values[6]
            models.append(model)

        homework_models.Homework.objects.bulk_create(models)

    def save_wronganswer_models(self, ws):

        models = []

        for i in range(ws.nrows):

            if i == 0:
                continue

            # i번째 모델의 값 리스트.
            values = ws.row_values(i, 0)

            model = homework_models.WrongAnswer()
            model.pk = int(values[0])
            model.created_at = datetime.datetime.fromtimestamp(
                int(values[1]))
            model.updated_at = datetime.datetime.fromtimestamp(
                int(values[2]))
            model.user = user_models.User.objects.get(
                pk=values[3])
            model.homework = homework_models.Homework.objects.get(pk=values[4])
            model.wrong_answer_string = values[5]
            models.append(model)

        homework_models.WrongAnswer.objects.bulk_create(models)


class TestView(View):

    def get(self, reqeust):

        # FILE_PATH = "assets/class_information.xls"
        # wb = xlrd.open_workbook(FILE_PATH)
        # num_of_sheet = len(wb.sheet_names())

        # for sheet_index in range(len(wb.sheet_names())):

        #     if wb.sheet_names()[sheet_index] != "User":
        #         continue

        #     ws = wb.sheet_by_index(sheet_index)

        #     for row_index in range(ws.nrows):
        #         values = ws.row_values(row_index, 0)
        #         print(values)

        return JsonResponse({
            "result": True,
        })
