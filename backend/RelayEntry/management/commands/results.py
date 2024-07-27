from django.core.management.base import BaseCommand
from RelayEntry.models import Team, Result
from datetime import datetime

class Command(BaseCommand):
    help = 'Create results for a team'

    def add_arguments(self, parser):
        parser.add_argument('team_name', type=str, help='The name of the team')
        parser.add_argument('times', type=str, help='Comma-separated times for the 4 legs')

    def handle(self, *args, **kwargs):
        team_name = kwargs['team_name']
        times_input = kwargs['times']
        times = [int(time.strip()) for time in times_input.split(',')]

        # Check if the length of the times array is 4
        if len(times) != 4:
            self.stdout.write(self.style.ERROR("Please provide exactly 4 times."))
            return

        # Find the team
        try:
            team = Team.objects.get(name=team_name)
        except Team.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Team with name '{team_name}' does not exist."))
            return

        race = team.race  # Assuming each team has a related race

        # Create results for each leg
        for index, time in enumerate(times, start=1):
            result = Result.objects.create(
                team=team,
                race=race,
                leg=index,
                time=time,
            )
            self.stdout.write(self.style.SUCCESS(f"Created result for leg {index}: {result}"))

