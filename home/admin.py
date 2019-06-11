from django.contrib import admin
from .models import Tournament, Institution, Team, Adjudicator, Venue

admin.site.register(Tournament)
admin.site.register(Institution)
admin.site.register(Team)
admin.site.register(Adjudicator)
admin.site.register(Venue)