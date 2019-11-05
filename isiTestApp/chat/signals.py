from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


from .models import Thread


@receiver(post_save, sender=Thread)
def thread_receiver(sender, instance, **kwargs):
    participants = instance.participants.all()
    if len(participants) > settings.CHAT_PARTICIPANTS:
        from django.core.exceptions import ValidationError
        raise ValidationError('Too much participants in Thread')
