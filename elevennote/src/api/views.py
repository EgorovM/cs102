from django.http import JsonResponse
from rest_framework import viewsets, status
from accounts.models import User
from notes.models import Note
from .serializers import NoteSerializer

from django.core import serializers

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def filter_queryset(self, queryset):
        queryset = Note.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = User.objects.all()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def filter_note(request, name):
    if request.method == "GET":
        notes = Note.objects.filter(
            tags__contains=name
        )

        notes |= Note.objects.filter(
            title__contains=name
        )

        return JsonResponse(serializers.serialize('json', list(notes)), safe=False,)


def share_note(request, pk, user_id):
    if request.method == "GET":
        note = Note.objects.get(pk=pk)
        if request.user != note.owner:
            return JsonResponse({"error", "not owner"}, code=400)

        note.shared.add(User.objects.get(id=user_id))
        note.save()

        return JsonResponse(serializers.serialize('json', list(note)))
