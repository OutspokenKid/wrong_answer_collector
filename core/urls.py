from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    # 기본 url로 들어올 경우 core/views.py의 MainView 클래스로 연결.
    path("", views.MainView.as_view(), name="main"),
]
