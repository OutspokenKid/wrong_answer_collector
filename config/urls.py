from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("classes/", include("classes.urls", namespace="classes")),
    path("users/", include("users.urls", namespace="users")),
    path('admin/', admin.site.urls),
]
