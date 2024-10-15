from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.forms import SimpleArrayField
from .models import Race

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RaceAdminForm(forms.ModelForm):
    projected_time_choices = SimpleArrayField(
        base_field=forms.CharField(),
        delimiter=',',
        required=False,
        help_text='Enter choices separated by commas.'
    )

    class Meta:
        model = Race
        fields = '__all__'