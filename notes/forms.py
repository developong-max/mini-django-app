from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Note title"}),
            "content": forms.Textarea(attrs={"rows": 6, "placeholder": "Write your note here..."}),
        }
