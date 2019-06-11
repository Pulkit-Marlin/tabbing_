import csv, io
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView
from .models import Tournament, Adjudicator, Team, Institution, Venue
from .forms import UserForm
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


class Rounds(generic.DetailView):
    model = Tournament
    template_name = 'home/rounds.html'


class Breaks(generic.DetailView):
    model = Tournament
    template_name = 'home/breaks.html'


class BreakRounds(generic.DetailView):
    model = Tournament
    template_name = 'home/breakrounds.html'


class Motions(generic.DetailView):
    model = Tournament
    template_name = 'home/motions.html'


class Settings(generic.DetailView):
    model = Tournament
    template_name = 'home/settings.html'


class Standings(generic.DetailView):
    model = Tournament
    template_name = 'home/standings.html'


# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'home/registration_form.html'
#
#     # display a blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#
#             user = form.save(commit=False)
#
#             # cleaned (normalized) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#
#             # returns User objects if credentials are correct
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#
#                 if user.is_active:
#
#                     login(request, user)
#                     return redirect('home:login')
#
#         return render(request, self.template_name, {'form': form})


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
            participants_name = column[1],
            institution_name = column[2],
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

