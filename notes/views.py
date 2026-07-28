from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NoteForm
from .models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            messages.success(request, "Note created.")
            return redirect("note_detail", pk=note.pk)
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form})


def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted.")
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})
