from rest_framework import serializers
from .models import Event, Race

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'url_alias', 'waiver_text', 'logo']

class RaceSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Race
        fields = '__all__'

class EventWithRacesSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
