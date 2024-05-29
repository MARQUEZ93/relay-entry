# my_app/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Race, Team, Registration, CouponCode, Document, PhotoPackage

class UserCreatedMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.created_by == self.request.user

class EventListView(LoginRequiredMixin, ListView):
    model = Event

    def get_queryset(self):
        if self.request.user.is_staff:
            return Event.objects.all()
        return Event.objects.filter(created_by=self.request.user)

class EventDetailView(LoginRequiredMixin, UserCreatedMixin, DetailView):
    model = Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'published', 'address', 'city', 'state', 'postal_code', 'google_maps_link', 'media_file', 'logo', 'waivers', 'facebook_url', 'instagram_url', 'twitter_url', 'email_url', 'website_url']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserCreatedMixin, UpdateView):
    model = Event
    fields = ['name', 'date', 'published', 'address', 'city', 'state', 'postal_code', 'google_maps_link', 'media_file', 'logo', 'waivers', 'facebook_url', 'instagram_url', 'twitter_url', 'email_url', 'website_url']

class EventDeleteView(LoginRequiredMixin, UserCreatedMixin, DeleteView):
    model = Event
    success_url = '/events/'  # Change to your desired URL

# Repeat similar views for other models like Race, Team, Registration, CouponCode, Document, PhotoPackage
