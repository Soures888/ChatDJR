from django.urls import path
from .views import ThreadPostView, MessageView, \
    ThreadGetView, ReadMessageView, UnreadMessagesView

urlpatterns = [
    path('create_chat/', ThreadPostView.as_view(), name='create_chat'),
    path('chats/', ThreadGetView.as_view(), name='view_chats'),
    path('messages/<int:pk>/', MessageView.as_view(), name='messages'),
    path('read_message/<int:pk>/', ReadMessageView.as_view(), name='read_message'),
    path('get_unread_messages/', UnreadMessagesView.as_view(), name='get_unread_messages')
]
