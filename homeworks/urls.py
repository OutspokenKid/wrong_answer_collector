from django.urls import path
from . import views

app_name = "homeworks"

urlpatterns = [

    path("", views.HomeworkListView.as_view(), name="homework_list"),
    path("<int:pk>", views.HomeworkDetailView.as_view(), name="homework_detail"),
    path("new", views.NewHomeworkView.as_view(), name="new_homework"),

    path("wrong_answer/", views.WrongAnswerListView.as_view(),
         name="wrong_answer_list"),
    path("wrong_andwer/new/<int:pk>",
         views.NewWrongAnswerView.as_view(), name="new_wrong_answer"),
]
