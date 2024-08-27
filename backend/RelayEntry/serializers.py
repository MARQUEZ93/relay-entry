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

    def validate_members(self, value):
        if not value:
            raise serializers.ValidationError("Members cannot be empty.")
        return value

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members')
        instance.name = validated_data.get('name', instance.name)
        instance.projected_team_time = validated_data.get('projected_team_time', instance.projected_team_time)
        instance.save()

        for member_data in members_data:
            member, created = TeamMember.objects.update_or_create(
                team=instance,
                email=member_data['email'],
                defaults={'leg_order': member_data['leg_order']}
            )

        return instance
    # TODO:
    # 1) Test email system to new member + captain
    # 2) same email validations (other teams etc or same team)
    # 3) is TM created or updated?
    # 4) ensure TM is deleted

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
    