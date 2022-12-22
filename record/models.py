from django.db import models
from django.conf import settings


class Record(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    money = models.BigIntegerField()
    detail_info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "records"


class ShortURL(models.Model):
    original_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=255)
    url_string = models.CharField(max_length=255)
    valid_time = models.DateTimeField()

    class Meta:
        db_table = "shortURLs"
