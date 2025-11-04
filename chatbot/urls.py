from django.urls import path
from chatbot import views

urlpatterns = [
   
    path('', views.redirect_to_chatbot),  # redirects root "/" to "/chatbot/"
    path('apply/', views.apply, name='apply'),
    path('form/', views.form, name='form'),
    path('fees/', views.fees, name='fees'),
    path('library/', views.library, name='library'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.upcoming_events, name='upcoming_events'),
    path('college/', views.college, name='college'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('career/', views.career, name='career'),
    path('placement/', views.placement, name='placement'),
    path('career/', views.career, name='career'),
path('careers/', views.career),  # optional alias
path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
]
