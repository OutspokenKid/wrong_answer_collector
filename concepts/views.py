from django.http import JsonResponse
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
        ids = concept.get_concept_video_ids()

        thumbnails = []
        urls = []
        titles = []

        video_index = 1

        for id in ids:
            thumbnails.append(
                f"https://img.youtube.com/vi/{id}/maxresdefault.jpg")
            urls.append(f"https://www.youtube.com/watch?v={id}")

            if len(ids) > 1:
                titles.append(
                    f"{concept.get_title_with_number()}({video_index})")
                video_index += 1
            else:
                titles.append(f"{concept.get_title_with_number()}")

        zip_for_video = zip(
            thumbnails,
            urls,
            titles,
        )

        return render(
            request,
            "concepts/concept_detail.html",
            {
                "concept": concept,
                "zip_for_video": zip_for_video,
            },
        )


class AddConceptVideoId(View):

    def post(self, request, pk):

        concept = get_object_or_404(models.Concept, pk=pk)
        video_id = request.POST.get("video_id", None)

        if not video_id:
            return JsonResponse({
                "result": False,
            })

        ids = concept.get_concept_video_ids()
        ids.append(video_id)
        concept.save_concept_video_ids(ids)
        concept.save()

        return JsonResponse({
            "result": True,
        })
