from django.contrib.auth.models import User
from django import forms
from .models import Institution, Team, Adjudicator, Venue


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class Upload_Institution_Form(forms.ModelForm):
    institution_name = forms.CharField(max_length=100)
    number_of_teams = forms.CharField(max_length=100)

    class Meta:
        model = Institution
        fields = ('institution_name', 'number_of_teams')


class Upload_Team_Form(forms.ModelForm):
    team_name = forms.CharField(max_length=100)
    participants_name_1 = forms.CharField(max_length=100)
    participants_name_2 = forms.CharField(max_length=100)
    institution_name = forms.CharField(max_length=100)

    class Meta:
        model = Team
        fields = ('team_name', 'participants_name_1', 'participants_name_2', 'institution_name')


class Upload_Adjudicator_Form(forms.ModelForm):
    adjudicator_name = forms.CharField(max_length=100)
    adjudicator_institution = forms.CharField(max_length=100)

    class Meta:
        model = Adjudicator
        fields = ('adjudicator_name', 'adjudicator_institution')

class Upload_Venue_Form(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = Institution
        fields = ('name',)