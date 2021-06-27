import binascii
import os

from django.db import models

# Create your models here.


class UserTokenModel(models.Model):
    user_id = models.UUIDField(null=False, blank=False)
    key = models.CharField(max_length=64, null=False, blank=False)
    is_valid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()
