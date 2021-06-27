import uuid

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    mobile = models.CharField(max_length=16)
    is_student = models.BooleanField(default=False)
