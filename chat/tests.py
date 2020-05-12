from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from django.core.exceptions import ValidationError

from .models import Thread


# Create your tests here.
class ThreadViewSetTestCase(APITestCase):
    def setUp(self):
        self.create_token_url = reverse('create-token')
        self.user = User.objects.create_user(username='isitest', password='very_strong_password')
        self.user.save()

        self.second_user = User.objects.create_user(username='isitest2', password='very_strong_password')
        self.second_user.save()

        self.third_user = User.objects.create_user(username='isitest3', password='very_strong_password')
        self.third_user.save()

        resp = self.client.post(self.create_token_url, {'username': 'isitest', 'password': 'very_strong_password'},
                                format='json')
        self.token = resp.data['token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

    def test_create_thread(self):
        url = reverse('create_chat')

        # Without data
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # With unknown data
        resp = self.client.post(url, data={"with_user": 34}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # With data
        resp = self.client.post(url, data={"with_user": 2}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_delete_thread(self):
        delete_chat = reverse('delete_chat', kwargs={"pk": 1})
        create_chat = reverse('create_chat')

        # With invalid pk
        resp = self.client.delete(delete_chat)
        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)

        # create chat
        resp = self.client.post(create_chat, data={"with_user": 2}, format='json')

        # Third user
        resp = self.client.post(self.create_token_url,
                                {'username': 'isitest3', 'password': 'very_strong_password'}, format='json')
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))

        resp = self.client.delete(delete_chat)
        self.assertEqual(status.HTTP_403_FORBIDDEN, resp.status_code)

        # Second user
        resp = self.client.post(self.create_token_url,
                                {'username': 'isitest2', 'password': 'very_strong_password'}, format='json')
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        resp = self.client.delete(delete_chat)
        self.assertEqual(status.HTTP_204_NO_CONTENT, resp.status_code)

    def test_get_thread(self):
        view_chat_url = reverse('view_chats')
        create_chat_url = reverse('create_chat')

        # Without chats
        resp = self.client.get(view_chat_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['results'], [])

        # Create chat
        resp = self.client.post(create_chat_url, data={"with_user": 2}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Get chats
        resp = self.client.get(view_chat_url)
        self.assertEqual(resp.data['count'], 1)


class MessageViewSetTestCase(APITestCase):
    def setUp(self):
        self.create_token_url = reverse('create-token')
        self.user = User.objects.create_user(username='isitest', password='very_strong_password')
        self.user.save()

        self.second_user = User.objects.create_user(username='isitest2', password='very_strong_password')
        self.second_user.save()

        self.third_user = User.objects.create_user(username='isitest3', password='very_strong_password')
        self.third_user.save()

        resp = self.client.post(self.create_token_url, {'username': 'isitest', 'password': 'very_strong_password'},
                                format='json')
        self.token = resp.data['token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

    def test_get_messages_for_thread(self):
        message_url = reverse('messages', kwargs={'pk': 1})
        create_chat_url = reverse('create_chat')

        # Get messages from thread: 1
        resp = self.client.get(message_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        # Create thread and get messages
        resp = self.client.post(create_chat_url, data={"with_user": 2}, format='json')
        resp = self.client.get(message_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Send message without text
        resp = self.client.post(message_url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # With text
        test_text = 'Hello world'
        resp = self.client.post(message_url, {'message': test_text})
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # Other user
        resp = self.client.post(self.create_token_url,
                                {'username': 'isitest3', 'password': 'very_strong_password'}, format='json')
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))

        # Get our message for another user
        resp = self.client.get(message_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_read_message(self):
        message_url = reverse('messages', kwargs={'pk': 1})
        create_chat_url = reverse('create_chat')
        read_url = reverse('read_messages')

        # Create Thread
        resp = self.client.post(create_chat_url, data={"with_user": 2}, format='json')

        # Send message
        test_text = 'Hello world Bro'
        resp = self.client.post(message_url, {'message': test_text})

        # We cannot send flag is_read to our message
        resp = self.client.post(read_url, {"messages_list": [1]}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        # Other user
        resp = self.client.post(self.create_token_url,
                                {'username': 'isitest2', 'password': 'very_strong_password'}, format='json')
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))

        # Send is_read flag
        resp = self.client.post(read_url, {"messages_list": [1]}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Messages
        resp = self.client.get(message_url)
        self.assertTrue(resp.data['results'][0]['is_read'])

    def test_unread_message_num(self):
        unread_message_url = reverse('get_unread_messages')
        message_url = reverse('messages', kwargs={'pk': 1})
        create_chat_url = reverse('create_chat')

        # Get unread messages
        resp = self.client.get(unread_message_url)
        self.assertEqual(resp.data['unread_messages'], 0)

        # Create Thread
        resp = self.client.post(create_chat_url, data={"with_user": 2}, format='json')

        # Send message
        test_text = 'Hello world Bro'
        resp = self.client.post(message_url, {'message': test_text})
        resp = self.client.get(unread_message_url)
        self.assertEqual(resp.data['unread_messages'], 0)

        # Other user
        resp = self.client.post(self.create_token_url,
                                {'username': 'isitest2', 'password': 'very_strong_password'}, format='json')
        token = resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        resp = self.client.get(unread_message_url)
        self.assertEqual(resp.data['unread_messages'], 1)


class SignalTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='isitest', password='very_strong_password')
        self.user.save()

        self.second_user = User.objects.create_user(username='isitest2', password='very_strong_password')
        self.second_user.save()

        self.third_user = User.objects.create_user(username='isitest3', password='very_strong_password')
        self.second_user.save()

    def test_signal(self):
        instance = Thread.objects.create()
        instance.participants.add(self.user, self.second_user, self.third_user)
        with self.assertRaises(ValidationError):
            instance.save()
