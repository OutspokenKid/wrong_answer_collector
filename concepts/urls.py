from django.urls import path
from . import views

app_name = "concepts"

urlpatterns = [
    path("", views.ConceptListView.as_view(), name="concept_list"),
    path("<int:pk>", views.ConceptDetailView.as_view(), name="concept_detail"),
]
