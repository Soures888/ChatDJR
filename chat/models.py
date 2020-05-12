from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    participants = models.ManyToManyField(User, verbose_name="Participants")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")


class Message(models.Model):
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, verbose_name="Thread", related_name="message_list", on_delete=models.CASCADE)

    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(verbose_name="Readed", default=False)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Message Date")
    updated = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.message
