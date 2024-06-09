from rest_framework import serializers
from .models import Event, Race

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'
class EventSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True, read_only=True)  # Add related races
    class Meta:
        model = Event
        fields = '__all__'
