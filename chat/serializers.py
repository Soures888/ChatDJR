from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Thread, Message

from django.conf import settings
from django.contrib.auth.models import User


class ThreadPostSerializer(serializers.ModelSerializer):
    with_user = serializers.IntegerField(write_only=True)
    """
    To serialize thread creation
    """

    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('created', 'updated', 'participants')

    def validate(self, attrs):
        """
        Validate data
        """
        participants = []

        # Verify user
        with_user = get_object_or_404(User, pk=attrs['with_user'])
        participants.append(with_user)

        # Add our user to the list of participants
        participants.append(self.context['request'].user)

        if len(participants) != settings.CHAT_PARTICIPANTS \
                or any(participants.count(x) > 1 for x in participants):
            # If the participants are not the right number or there are repetitions
            raise serializers.ValidationError({"errors": "participants validation error"})

        attrs['participants'] = participants

        return attrs

    def create(self, validated_data):
        part_data = validated_data.get('participants')
        instance = Thread.objects.filter(participants=part_data[0]).filter(participants=part_data[1]).first()

        if instance:
            return instance

        many_to_many = validated_data.pop('participants')
        _ = validated_data.pop('with_user')
        instance = Thread.objects.create(**validated_data)

        for user in many_to_many:
            instance.participants.add(user)

        return instance


class ThreadGetSerializer(serializers.ModelSerializer):
    """
    To serialize receiving messages
    """
    last_message = serializers.SerializerMethodField('get_last_message')

    @classmethod
    def get_last_message(self, thread):
        qs = Message.objects.filter(thread=thread).last()
        if not qs:
            # If there is no last message, return None
            return None
        serializer = MessageSerializer(instance=qs, many=False)
        return serializer.data

    class Meta:
        model = Thread
        fields = ('id', 'participants', 'created', 'updated', 'last_message')


class MessageSerializer(serializers.ModelSerializer):
    """
    To serialize messages
    """
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ('__all__')
        read_only_fields = ('id', 'is_read', 'created', 'updated', 'thread', 'sender')

    def validate(self, attrs):
        """
        Validate data
        """

        # Get user from post
        user = self.context['request'].user

        # Get pk from url for post
        pk_thread_id = self.context['view'].kwargs.get('pk')

        # Thread Check
        thread = Thread.objects.filter(pk=pk_thread_id, participants=user).first()

        if not thread:
            # If we do not find the desired Thread or User does not have access
            raise serializers.ValidationError({'errors': 'not true thread_id / no access rights to thread'})

        attrs['sender'] = user
        attrs['thread'] = thread

        return attrs


class ReadMessageSerializer(serializers.ModelSerializer):
    """
    To serialize the flag 'is_read'
    """

    class Meta:
        model = Message
        fields = ('id', 'is_read')
        read_only_fields = ('id', 'is_read')
