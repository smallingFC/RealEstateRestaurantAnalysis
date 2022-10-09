from django.urls import path
from . import views

urlpatterns = [
     
    path('',views.login, name='login'),
    path('register',views.register, name='register'),    
    path('index',views.home, name='index'),    
    path('properties',views.properties,name='properties'),
    path('analysis',views.analysis,name='analysis'), 
    path('sell',views.sell,name='sell'),
]