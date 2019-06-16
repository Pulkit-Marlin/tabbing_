import csv, io
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView
from .models import Tournament, Adjudicator, Team, Institution, Venue
from .forms import UserForm, Upload_Institution_Form, Upload_Adjudicator_Form, Upload_Team_Form, Upload_Venue_Form
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class Homepage(generic.ListView):
    template_name = 'home/homepage.html'
    context_object_name = 'all_tournaments'

    def get_queryset(self):
        return Tournament.objects.filter(user = self.request.user)



class DetailView(generic.DetailView):
    model = Tournament
    template_name = 'home/detail.html'

    # def get_context_data(self, pk):
    #     context = super().get_context_data(pk)
    #     context['tournament_id'] = Tournament.objects.filter(id = pk).get()
    #     return context

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament' : Tournament.objects.filter(id = pk).get()
        }
        return render(request, self.template_name, args)



class WelcomePage(generic.ListView):
    model = Tournament
    template_name = 'home/welcome_page.html'


class TournamentCreate(LoginRequiredMixin,CreateView):
    model = Tournament
    fields = ['tournament_name', 'dates', 'speaker_score_range', 'adjudicator_score_range', 'number_of_rounds', 'number_of_break_rounds', 'tournament_venue']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class Participants(generic.DetailView):
    model = Tournament
    template_name = 'home/participants.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)



class Rounds(generic.DetailView):
    model = Tournament
    template_name = 'home/rounds.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)



class Breaks(generic.DetailView):
    model = Tournament
    template_name = 'home/breaks.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)


class BreakRounds(generic.DetailView):
    model = Tournament
    template_name = 'home/breakrounds.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)



class Motions(generic.DetailView):
    model = Tournament
    template_name = 'home/motions.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)



class Settings(generic.DetailView):
    model = Tournament
    template_name = 'home/settings.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get()
        }
        return render(request, self.template_name, args)

#
# class Standings(generic.DetailView):
#     model = Tournament
#     template_name = 'home/standings.html'
#
#     def get(self, request, pk):
#         args = {
#             'tournament_id': pk,
#             'tournament': Tournament.objects.filter(id=pk).get()
#         }
#         return render(request, self.template_name, args)


class TeamStandings(generic.DetailView):
    model = Tournament
    template_name = 'home/team-standings.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get(),
            'all_teams': Team.objects.filter(tournament = pk).order_by('score')
        }
        return render(request, self.template_name, args)



class AdjudicatorStandings(generic.DetailView):
    model = Tournament
    template_name = 'home/adjudicator-standings.html'

    def get(self, request, pk):
        args = {
            'tournament_id': pk,
            'tournament': Tournament.objects.filter(id=pk).get(),
            'all_adjudicators': Adjudicator.objects.filter(tournament=pk).order_by('score')
        }
        return render(request, self.template_name, args)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log the user in
            login(request, user)
            return redirect('home:homepage')

    else:
        form = UserCreationForm()

    return render(request, 'home/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log the user in
            user = form.get_user()
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home:homepage')


    else:
        form = AuthenticationForm()

    return render(request, 'home/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:welcome')


def upload(request,pk):
    template = 'home/upload.html'
    args = {'tournament_id': pk}

    return render(request, template, args)


def upload_institution(request,pk):
    template = "home/upload-institution.html"
    template2 = "home/upload.html"

    prompt = {
        'order': 'Order of the CSV should be Institution name, Number of teams in the Institute',
        'tournament_id': pk
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Institution.objects.update_or_create(
            tournament = Tournament.objects.filter(id=pk).get(),
            institution_name = column[0],
            number_of_teams = column[1],
        )

    args = {'tournament_id': pk}
    return render(request, template2, args)

def upload_team(request,pk):
    template = "home/upload-team.html"
    template2 = "home/upload.html"

    prompt = {
        'order': 'Order of the CSV should be Team name, Name of Participants, Institution the team belongs to',
        'tournament_id': pk
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Team.objects.update_or_create(
            tournament=Tournament.objects.filter(id=pk).get(),
            team_name = column[0],
            participants_name_1 = column[1],
            participants_name_2 = column[2],
            institution_name = column[3],
        )

    args = {'tournament_id': pk}
    return render(request, template2, args)

def upload_adjudicator(request,pk):
    template = "home/upload-adjudicator.html"
    template2 = "home/upload.html"

    prompt = {
        'order': 'Order of the CSV should be Name, Institution the Judge belongs to',
        'tournament_id': pk
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Adjudicator.objects.update_or_create(
            tournament=Tournament.objects.filter(id=pk).get(),
            adjudicator_name = column[0],
            adjudicator_institution = column[1],
        )

    args = {'tournament_id': pk}
    return render(request, template2, args)

def upload_venue(request,pk):
    template = "home/upload-venue.html"
    template2 = "home/upload.html"

    prompt = {
        'order': 'Order of the CSV should be Name',
        'tournament_id': pk
    }

    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Venue.objects.update_or_create(
            tournament=Tournament.objects.filter(id=pk).get(),
            name = column[0],
            #address = column[1],
        )

    args = {'tournament_id': pk}
    return render(request, template2, args)


class Upload_Institution_Manually(TemplateView):
    template = "home/upload-institution-manually.html"

    def get(self, request, pk):
        form = Upload_Institution_Form()
        args = {'form': form}
        return render(request, self.template, args)

    def post(self, request, pk):
        form = Upload_Institution_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tournament = Tournament.objects.filter(id=pk).get()
            post.save()

            return redirect('home:upload', pk)

        args = {'form': form}
        return render(request, self.template, args)


class Upload_Team_Manually(TemplateView):
    template = "home/upload-team-manually.html"

    def get(self, request, pk):
        form = Upload_Team_Form()
        args = {'form': form}
        return render(request, self.template, args)

    def post(self, request, pk):
        form = Upload_Team_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tournament = Tournament.objects.filter(id=pk).get()
            post.save()

            return redirect('home:upload', pk)

        args = {'form': form}
        return render(request, self.template, args)


class Upload_Adjudicator_Manually(TemplateView):
    template = "home/upload-adjudicator-manually.html"

    def get(self, request, pk):
        form = Upload_Adjudicator_Form()
        args = {'form': form}
        return render(request, self.template, args)

    def post(self, request, pk):
        form = Upload_Adjudicator_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tournament = Tournament.objects.filter(id=pk).get()
            post.save()

            return redirect('home:upload', pk)

        args = {'form': form}
        return render(request, self.template, args)


class Upload_Venue_Manually(TemplateView):
    template = "home/upload-venue-manually.html"

    def get(self, request, pk):
        form = Upload_Venue_Form()
        args = {'form': form}
        return render(request, self.template, args)

    def post(self, request, pk):
        form = Upload_Venue_Form(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.tournament = Tournament.objects.filter(id=pk).get()
            post.save()

            return redirect('home:upload', pk)

        args = {'form': form}
        return render(request, self.template, args)

