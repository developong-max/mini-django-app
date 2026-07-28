from django.urls import path

from . import views

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("note/new/", views.note_create, name="note_create"),
    path("note/<int:pk>/", views.note_detail, name="note_detail"),
    path("note/<int:pk>/delete/", views.note_delete, name="note_delete"),
]
