from django.shortcuts import redirect

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.urls import reverse, reverse_lazy

from .models import Note
from .mixins import NoteMixin
from .forms  import NoteForm


User = get_user_model()


class NoteList(LoginRequiredMixin, ListView):
    paginate_by = 5
    template_name = 'notes/index.html'
    context_object_name = 'latest_note_list'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        notes = list(Note.objects.filter(
            owner=self.request.user,
            tags__contains=self.request.GET.get('filter_tag', ''),
            title__contains=self.request.GET.get('filter_name', ''),
        ))

        notes.extend(list(Note.objects.filter(
            shared__id__exact=self.request.user.id
        )))

        notes.sort(key=lambda x: x.pub_date, reverse=True)

        return notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()

        return context

class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/detail.html'
    context_object_name = 'note'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteDetail, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteCreate(LoginRequiredMixin, NoteMixin, CreateView):
    form_class = NoteForm
    template_name = 'notes/form.html'
    success_url = reverse_lazy('notes:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.pub_date = timezone.now()

        return super(NoteCreate, self).form_valid(form)


class NoteUpdate(LoginRequiredMixin, NoteMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/form.html'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('notes:update', kwargs={
          'pk': self.object.pk })


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('notes:create')

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


def share_note(request, pk):
    note = Note.objects.get(id=pk)

    msg = "Fail :("

    if request.method == "POST":
        user_id = request.POST['user_id']
        user = User.objects.get(id=user_id)
        note.shared.add(user)
        msg = f"You share {note.title} to {user.email}!"

    return redirect(f"/notes?msg={msg}")
