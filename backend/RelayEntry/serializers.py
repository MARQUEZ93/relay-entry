from rest_framework import serializers
from .models import Event, Race, Team, TeamMember, Registration, Result
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['first_name', 'last_name']

class TeamMemberSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer(source='registration_set', many=True, read_only=True)
    class Meta:
        model = TeamMember
        fields = ['id', 'email', 'leg_order', 'registration']

class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    captain = RegistrationSerializer(read_only=True)
    class Meta:
        model = Team
        fields = ['id', 'name', 'captain', 'projected_team_time', 'members']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'url_alias', 'waiver_text', 'logo']

class RaceSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Race
        fields = '__all__'

class EventWithRacesSerializer(serializers.ModelSerializer):
    races = RaceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    registrant = RegistrationSerializer()

    class Meta:
        model = Result
        fields = ['registrant', 'time', 'leg_order', 'is_team_total']

class TeamResultSerializer(serializers.ModelSerializer):
    team_result = ResultSerializer()
    leg_results = ResultSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'team_result', 'leg_results']
