from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Record

from datetime import datetime


class RecordSerializer(serializers.ModelSerializer):
    created_day = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ["id", "user", "money", "detail_info", "created_day","updated_at"]
        extra_kwargs = {"user": {"read_only": True}}

    def get_created_day(self, obj):
        """change format of created_at field data"""
        return datetime.strftime(obj.created_at,"%Y-%m-%d")

class CopyRecordSerialzier(RecordSerializer):
    """Serailizer for create new record with copied data"""
    
    class Meta(RecordSerializer.Meta):
        fields = ["user", "money", "detail_info"]
    