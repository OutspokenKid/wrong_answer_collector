from django.urls import path
from . import views

app_name = "classes"

urlpatterns = [

    path("", views.ClassListView.as_view(), name="class_list"),
    path("<int:pk>", views.ClassDetailView.as_view(), name="class_detail"),
    path("<int:pk>/info", views.ClassInfoView.as_view(), name="class_info"),
]
