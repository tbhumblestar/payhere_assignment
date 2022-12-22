from rest_framework import serializers
from .models import Record, ShortURL

from datetime import datetime


class RecordSerializer(serializers.ModelSerializer):
    created_day = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ["id", "user", "money", "detail_info", "created_day", "updated_at"]
        extra_kwargs = {"user": {"read_only": True}}

    def __init__(self, *args, **kwargs):
        """Filtering fields."""
        super().__init__(*args, **kwargs)
        want_fields = self.context.get("want_fields")

        if want_fields:
            allowed = set(want_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_created_day(self, obj):
        """change format of created_at field data"""
        return datetime.strftime(obj.created_at, "%Y-%m-%d")


class CopyRecordSerialzier(RecordSerializer):
    """Serailizer for create new record with copied data"""

    class Meta(RecordSerializer.Meta):
        fields = ["user", "money", "detail_info"]


class ShortCutURLSerializer(serializers.ModelSerializer):
    """Serailizer for shortcutURL"""

    class Meta:
        model = ShortURL
        fields = "__all__"

    def create(self, validated_data):
        original_url = validated_data.get("original_url")

        if ShortURL.objects.filter(original_url=original_url):
            shorturl = ShortURL.objects.get(original_url=original_url)
            shorturl.short_url = validated_data.get("short_url")
            shorturl.url_string = validated_data.get("url_string")
            shorturl.valid_time = validated_data.get("valid_time")
            shorturl.save()

        else:
            shorturl = ShortURL.objects.create(**validated_data)

        return shorturl
