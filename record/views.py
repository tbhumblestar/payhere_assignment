from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from record.models import Record
from record.serializers import RecordSerializer, CopyRecordSerialzier

from core.permissions import IsAdminOrIsWriterOrForbidden


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
