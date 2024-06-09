# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from .views import EventDetailView

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'),
    path('api<slug:url_alias>/', EventDetailView.as_view(), name='event-detail'),
    path('connect_stripe/', views.connect_stripe_account, name='connect_stripe'),
    path('stripe_callback/', views.stripe_callback, name='stripe_callback'),
    path('create-payment-intent/', views.create_payment_intent, name='create-payment-intent'),
    path('confirm-payment-intent/', views.confirm_payment_intent, name='confirm-payment-intent'),
]
