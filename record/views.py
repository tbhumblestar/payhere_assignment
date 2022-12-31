from django.shortcuts import get_object_or_404, redirect

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from record.models import Record, ShortURL
from record.serializers import (
    RecordSerializer,
    CopyRecordSerialzier,
    ShortCutURLSerializer,
)

from core.permissions import IsAdminOrIsWriterOrForbidden
from core.exceptions import ShortURLNotValidError

from datetime import datetime, timedelta

from random import choices
from string import ascii_letters


class RecordView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecordSerializer

    def get_queryset(self):
        """Filter authenticated user's queryset."""

        user = self.request.user
        queryset = Record.objects.filter(user=user).order_by("created_at")

        return queryset

    def copy_record(self, request) -> dict:
        """copy other record object data and return it as dict"""

        copy_record_id = request.query_params.get("copy_record_id")
        copy_record = get_object_or_404(Record, id=copy_record_id)

        if self.request.user != copy_record.user:
            raise PermissionDenied

        copy_serializer = CopyRecordSerialzier(instance=copy_record)

        return copy_serializer.data

    def create(self, request, *args, **kwargs):
        """validate data and save record  object"""

        data = request.data
        if request.query_params.get("copy_record_id"):
            data = self.copy_record(request)
            data.update(request.data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """Pass user_id and save record object."""

        user = self.request.user
        serializer.save(user=user)


class RecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrIsWriterOrForbidden,)
    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    lookup_url_kwarg = "record_id"


def making_original_url(self, request):
    """making_original_url for shortcutURL"""
    original_url = request.build_absolute_uri(request.path)
    if request.query_params.get("want_fields"):
        original_url += "?want_fields=" + request.query_params.get("want_fields")

    return original_url


def make_random_string(self):
    """make_random_string"""

    while True:
        url_string = "".join(choices(ascii_letters, k=7))
        if not ShortURL.objects.filter(url_string=url_string).exists():
            break

    return url_string


def making_short_url(self, request, url_string):
    """make ShortcutURL from originalURL"""

    short_url = (
        list(request.build_absolute_uri().split(":"))[0]
        + "://"
        + request.headers.get("Host")
        + "/"
        + url_string
        + "/"
    )

    return short_url


class ShortCutURLView(APIView):
    def get(self, request, *args, **kwargs):

        record_id = self.kwargs.get("record_id")
        record = get_object_or_404(Record, id=record_id)

        context = {}
        want_fields = self.request.query_params.get("want_fields")
        if want_fields:
            context["want_fields"] = tuple(want_fields.split(","))
        serializer = RecordSerializer(instance=record, context=context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """Change original_url to short_url and save them."""

        record_id = self.kwargs.get("record_id")
        record = get_object_or_404(Record, id=record_id)

        if self.request.user != record.user:
            raise PermissionDenied

        url_string = make_random_string(self)

        data = {
            "original_url": making_original_url(self, request),
            "short_url": making_short_url(self, request, url_string),
            "url_string": url_string,
            "valid_time": datetime.now()
            + timedelta(days=int(request.query_params.get("valid_day", 7))),
        }
        serializer = ShortCutURLSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Redirector(APIView):
    def get(self, request, *args, **kwargs):
        """Redirect shortURL to originalURL"""
        url_string = self.kwargs.get("short_url")
        shorturl = get_object_or_404(ShortURL, url_string=url_string)

        if datetime.now() > shorturl.valid_time:
            #데이터를 삭제해주는 것도 좋을 듯
            raise ShortURLNotValidError

        return redirect(shorturl.original_url)
