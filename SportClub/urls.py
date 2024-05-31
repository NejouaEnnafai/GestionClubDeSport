
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [ 
    path('authentification/', views.authentification, name='authentification'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('inscription/', views.inscription, name='inscription'),
    path('inscripEffect/', views.inscripEffect, name='inscripEffect'),
    path('inscriEvent/', views.inscriEvent, name='inscriEvent'),
    path('inscriActi/', views.inscriActi, name='inscriActi'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('inscriRes/', views.inscriRes, name='inscriRes'),
  
  
  
    
    
    

   
]