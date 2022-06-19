from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from classes import models as class_models
from . import models


class ConceptListView(View):

    def get(self, request):

        subject_pk = request.GET.get("subject_pk", -1)
        subjects = class_models.Subject.objects.all()
        concepts = models.Concept.objects.filter(subject=subject_pk)

        return render(
            request,
            "concepts/concept_list.html",
            {
                "subject_pk": int(subject_pk),
                "subjects": subjects,
                "concepts": concepts,
            },
        )


class ConceptDetailView(View):

    def get(self, request, pk):

        concept = get_object_or_404(models.Concept, pk=pk)

        return render(
            request,
            "concepts/concept_detail.html",
            {
                "concept": concept,
            },
        )
