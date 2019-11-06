import json

from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import serializers
from rest_framework import exceptions

from .models import Thread, Message
from .permissions import ThreadPermission
from isiTestApp.chat.serializers import ThreadPostSerializer, MessageSerializer, \
    ThreadGetSerializer, ReadMessageSerializer
from rest_framework.permissions import IsAuthenticated


class ThreadPostView(generics.CreateAPIView):
    """
    Create a Thread
    """
    serializer_class = ThreadPostSerializer
    model = Thread
    permission_classes = (IsAuthenticated,)


class ThreadDeleteView(generics.DestroyAPIView):
    """
    Destroy a Thread
    """
    model = Thread
    permission_classes = (IsAuthenticated, ThreadPermission)
    queryset = Thread.objects.all()


class ThreadGetView(generics.ListAPIView):
    """
    User Thread List
    """
    serializer_class = ThreadGetSerializer
    model = Thread
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        # Take Thread, if our user is there
        return self.model.objects.filter(participants=user).all()


class MessageView(generics.ListCreateAPIView):
    """
    Create a message for the thread
    Receive a messages from the thread
    """
    serializer_class = MessageSerializer
    model = Message
    permission_classes = (IsAuthenticated, ThreadPermission)

    def get_queryset(self):
        # We take only a specific Thread, and only if our user is there
        return self.model.objects.filter(thread__pk=self.kwargs['pk'],
                                         thread__participants=self.request.user).all()


class ReadMessageView(generics.CreateAPIView):
    """
    Toggle flag is_read
    """
    model = Message
    permission_classes = (IsAuthenticated,)
    serializer_class = ReadMessageSerializer

    def get_object(self):
        messages_list = self.request.data.get('messages_list')
        if not messages_list:
            raise exceptions.ValidationError({"error": "Invalid messages_list"})

        if not all(isinstance(item, int) for item in messages_list) \
                or not isinstance(messages_list, list):
            # Check that all numbers are int
            raise exceptions.ValidationError({"error": "Bad request data"})

        instances = Message.objects.exclude(sender=self.request.user). \
            filter(is_read=False, thread__participants=self.request.user,
                   pk__in=messages_list).all()

        if not instances:
            raise exceptions.NotFound({"error": "No valid messages"})

        return instances

    def create(self, request, *args, **kwargs):
        instances = self.get_object()

        for instance in instances:
            instance.is_read = True
            instance.save()

        serializer = ReadMessageSerializer(instances, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


class UnreadMessagesView(generics.ListAPIView):
    """
    Get the number of unread messages
    """
    model = Message
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # We receive messages not from our user, and that he would be in Thread
        queryset = self.model.objects.exclude(sender=self.request.user). \
            filter(is_read=False, thread__participants=self.request.user).all()
        response_data = {"unread_messages": len(queryset)}
        return Response(response_data, 200)
