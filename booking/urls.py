from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_lawyer, name='lawyer_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('approve/<int:pk>/', views.approve_appointment, name='approve_appointment'),
    path('decline/<int:pk>/', views.decline_appointment, name='decline_appointment'),
    path('complete/<int:pk>/', views.complete_appointment, name='complete_appointment'),
    path('chat/user/<int:user_id>/', views.chat, name='chat_for_lawyer'),
    path('chat/lawyer/<int:lawyer_id>/', views.chat, name='chat_for_user'),
    path('chat/<int:pk>/', views.chat_by_conversation, name='chat_by_conversation'),
]
