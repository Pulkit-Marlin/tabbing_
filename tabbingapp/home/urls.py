from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.WelcomePage.as_view(), name='welcome'),
    path('register/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('addtournament/', views.TournamentCreate.as_view(), name='add-tournament'),
    path('homepage/', views.Homepage.as_view(), name='homepage'),
    re_path(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    re_path(r'^(?P<pk>[0-9]+)/participants/$', views.Participants.as_view(), name='participants'),
    re_path(r'^(?P<pk>[0-9]+)/motions/$', views.Motions.as_view(), name='motions'),
    re_path(r'^(?P<pk>[0-9]+)/settings/$', views.Settings.as_view(), name='settings'),
    re_path(r'^(?P<pk>[0-9]+)/rounds/$', views.Rounds.as_view(), name='rounds'),
    re_path(r'^(?P<pk>[0-9]+)/breaks/$', views.Breaks.as_view(), name='breaks'),
    re_path(r'^(?P<pk>[0-9]+)/standings/$', views.Standings.as_view(), name='standings'),
    re_path(r'^(?P<pk>[0-9]+)/breakrounds/$', views.BreakRounds.as_view(), name='breakrounds'),
    re_path(r'^(?P<pk>[0-9]+)/upload/$', views.upload, name="upload"),
    re_path(r'^(?P<pk>[0-9]+)/upload/institution$', views.upload_institution, name="upload_institution"),
    re_path(r'^(?P<pk>[0-9]+)/upload/team$', views.upload_team, name="upload_team"),
    re_path(r'^(?P<pk>[0-9]+)/upload/adjudicator$', views.upload_adjudicator, name="upload_adjudicator"),
    re_path(r'^(?P<pk>[0-9]+)/upload/venue$', views.upload_venue, name="upload_venue"),
    re_path(r'^(?P<pk>[0-9]+)/upload/institution_manually$', views.Upload_Institution_Manually.as_view(), name="upload_institution_manually"),
    re_path(r'^(?P<pk>[0-9]+)/upload/team_manually$', views.Upload_Team_Manually.as_view(), name="upload_team_manually"),
    re_path(r'^(?P<pk>[0-9]+)/upload/adjudicator_manually$', views.Upload_Adjudicator_Manually.as_view(), name="upload_adjudicator_manually"),
    re_path(r'^(?P<pk>[0-9]+)/upload/venue_manually$', views.Upload_Venue_Manually.as_view(), name="upload_venue_manually"),
]
