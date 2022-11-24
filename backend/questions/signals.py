from .models import Question
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify


@receiver(pre_save, sender=Question)
def add_slug(sender, instanse, *args, **kwrgs):
    if instanse and not instanse.slug:
        slug = slugify(instanse.content)
        random_string = get_random_string(length=8)
        instanse.slug = slug + "-" + random_string
