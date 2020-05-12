from django.urls import path
from .views import ThreadPostView, MessageView, \
    ThreadGetView, ReadMessageView, UnreadMessagesView, ThreadDeleteView

urlpatterns = [
    path('create_chat/', ThreadPostView.as_view(), name='create_chat'),
    path('delete_chat/<int:pk>/', ThreadDeleteView.as_view(), name='delete_chat'),
    path('chats/', ThreadGetView.as_view(), name='view_chats'),
    path('messages/<int:pk>/', MessageView.as_view(), name='messages'),
    path('read_messages/', ReadMessageView.as_view(), name='read_messages'),
    path('get_unread_messages/', UnreadMessagesView.as_view(), name='get_unread_messages')
]
