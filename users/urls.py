from django.urls import path
from . import views

app_name = "users"

urlpatterns = [

    path("sign_in", views.SignInView.as_view(), name="sign_in"),
    path("sign_out", views.SignOutView.as_view(), name="sign_out"),
]
