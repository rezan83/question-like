import uuid as uuid_lib
from django.db import models
from custom_models.models import TimeStampModel
from django.conf import settings


class Question(TimeStampModel):

    content = models.CharField(max_length=250)
    slug = models.SlugField(max_length=258, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")

    def __str__(self) -> str:
        return self.content


class Answer(TimeStampModel):
    uuid = models.UUIDField(
        db_index=True, default=uuid_lib.uuid4, editable=False)
    content = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers")
    voter = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  related_name="likes")

    def __str__(self) -> str:
        return self.author.username
