import uuid

from django.db import models

from doubt.choices import DoubtStateChoices
from users.models import CustomUser


# Create your models here.


class DoubtsModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False,
                             related_name='user_custom_user')
    question = models.TextField(null=False, blank=False, max_length=1000)
    title = models.TextField(null=False, blank=False, max_length=200)
    state = models.IntegerField(choices=DoubtStateChoices().CHOICES, default=DoubtStateChoices.DRAFT, null=False,
                                blank=False)
    ta = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=False,
                           related_name='ta_custom_user')
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_on = models.DateTimeField(auto_now=True, null=False, blank=False)
    resolved_on = models.DateTimeField(null=True, blank=False)
    picked_on = models.DateTimeField(null=True, blank=False)


class DoubtQnAModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    doubt = models.ForeignKey(DoubtsModel, on_delete=models.CASCADE, null=False, blank=False)
    is_answer = models.BooleanField()
    text = models.TextField(null=False, blank=False, max_length=1000)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
