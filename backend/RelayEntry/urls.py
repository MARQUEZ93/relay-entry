# backend/RelayEntry/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'),
    path('connect_stripe/', views.connect_stripe_account, name='connect_stripe'),
    path('stripe_callback/', views.stripe_callback, name='stripe_callback'),
]
