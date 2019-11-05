from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

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


class ReadMessageView(generics.UpdateAPIView):
    """
    Toggle flag is_read
    """
    model = Message
    permission_classes = (IsAuthenticated, )
    serializer_class = ReadMessageSerializer

    def get_queryset(self):
        # We take only an unread message to our user
        queryset = self.model.objects.exclude(sender=self.request.user). \
            filter(is_read=False, thread__participants=self.request.user, pk=self.kwargs['pk'])
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        instance = self.get_object()

        instance.is_read = True
        instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


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
