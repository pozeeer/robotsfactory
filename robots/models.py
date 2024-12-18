from django.db import models


class Robot(models.Model):
    STATUS_CHOICES = [
        ("sold", "Sold"),  # Продан
        ("available", "Available")  # В наличии
    ]

    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="available", blank=True, null=False)
