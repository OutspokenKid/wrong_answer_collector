from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    # 기본 url로 들어올 경우 core/views.py의 MainView 클래스로 연결.
    path("", views.MainView.as_view(), name="main"),

    path("admin_menu", views.AdminMenuView.as_view(), name="admin_menu"),
    path("extract_information", views.ExtractInformation.as_view(),
         name="extract_information"),
    path("load_information", views.LoadInformation.as_view(),
         name="load_information"),

    path("test", views.TestView.as_view(), name="test"),

    # path("", include("classes.urls", namespace="classes")),
]
