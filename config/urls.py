from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("classes/", include("classes.urls", namespace="classes")),
    path("homeworks/", include("homeworks.urls", namespace="homeworks")),
    path("concepts/", include("concepts.urls", namespace="concepts")),
    path("users/", include("users.urls", namespace="users")),
    path('admin/', admin.site.urls),
]

# 미디어 url 연결.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
