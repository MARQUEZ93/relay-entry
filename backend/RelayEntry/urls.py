# backend/RelayEntry/urls.py

from django.urls import path
from . import views
from .views import EventDetailView, RaceDetailView

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'),
    path('api/events/<slug:url_alias>/races/<int:id>/', RaceDetailView.as_view(), name='race-detail'),
    path('api/events/<slug:url_alias>/', EventDetailView.as_view(), name='event-detail'),
    path('api/create-payment-and-registration/', views.create_payment_and_registration, name='create-payment-intent'),
]
