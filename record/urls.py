from django.urls import path

from record import views

app_name = "record"

urlpatterns = [
    path("", views.RecordView.as_view(), name="record"),
    path("<int:record_id>/", views.RecordDetailView.as_view(), name="record-detail"),
    path(
        "<int:record_id>/shortcut/",
        views.ShortCutURLView.as_view(),
        name="record-shortcut",
    ),
]
