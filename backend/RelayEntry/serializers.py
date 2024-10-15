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
    complete = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id', 'name', 'captain', 'projected_time', 'members', 'complete']
    def get_complete(self, obj):
        return obj.complete()

class EventDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'name', 'description', 'date', 'end_date', 'address', 'city', 'state',
            'postal_code', 'email', 'waiver_text', 'facebook_url', 'instagram_url', 
            'twitter_url', 'website_url', 'published', 'registration_closed', 
            'logo', 'male_tshirt_image', 'female_tshirt_image', 'media_file',
        ]

    def validate(self, data):
        start_date = data.get('date')
        end_date = data.get('end_date')
        if (end_date and not start_date) or (end_date and end_date < start_date):
            raise serializers.ValidationError("End date must be after the start date.")
        return data
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'date', 'url_alias', 'waiver_text', 'logo', 'registration_closed']

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
    class Meta:
        model = Result
        fields = ['time', 'leg_order', 'is_team_total', 'place']

class TeamResultSerializer(serializers.ModelSerializer):
    team_result = serializers.SerializerMethodField()
    leg_results = serializers.SerializerMethodField()
    captain_name = serializers.SerializerMethodField()
    num_runners = serializers.SerializerMethodField()
    is_relay = serializers.SerializerMethodField()
    race_name = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'captain_name', 'team_result', 'leg_results', 'num_runners', 'is_relay', 'race_name']

    def get_team_result(self, obj):
        team_total_result = Result.objects.filter(team=obj, is_team_total=True).first()
        return ResultSerializer(team_total_result).data if team_total_result else None

    def get_leg_results(self, obj):
        leg_results = Result.objects.filter(team=obj, is_team_total=False)
        return ResultSerializer(leg_results, many=True).data

    def get_captain_name(self, obj):
        return f'{obj.captain.first_name} {obj.captain.last_name}'

    def get_num_runners(self, obj):
        return obj.race.num_runners

    def get_is_relay(self, obj):
        return obj.race.is_relay

    def get_race_name(self, obj):
        return obj.race.name

class RaceDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'
