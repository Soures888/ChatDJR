from .models import Thread
from rest_framework import permissions


class ThreadPermission(permissions.BasePermission):
    def __init__(self, ):
        super().__init__()

    def has_permission(self, request, view):
        thread_object = Thread.objects.filter(participants=request.user, pk=view.kwargs['pk']).first()
        if thread_object:
            return True
