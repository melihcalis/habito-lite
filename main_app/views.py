from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from .models import Habit, Log, Participation
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView


class IndexView(View):
    
    def get(self, request):
        if not request.user.is_authenticated:

            
            return render(request, "welcome.html")
            #return render(request, "index.html", context)
        
        users = User.objects.all()

        usernames = [user.username for user in users]

        participations = Participation.objects.all()

        logs = Log.objects.all()

        habits = Habit.objects.all()

        today = datetime.today().date()
        yesterday = datetime.today().date() - timedelta(days=1)
        day_3 = datetime.today().date() - timedelta(days=2)
        day_4 = datetime.today().date() - timedelta(days=3)
        day_5 = datetime.today().date() - timedelta(days=4)
        day_6 = datetime.today().date() - timedelta(days=5)
        day_7 = datetime.today().date() - timedelta(days=6)

        current_user = request.user

        habits_of_user = []

        for participation in participations:
            if participation.participant == current_user:
                habits_of_user.append(participation.habit)

        day_7_habits = []
        day_6_habits = []
        day_5_habits = []
        day_4_habits = []
        day_3_habits = []
        yesterday_habits = []
        today_habits = []

        for log in logs:
            if log.date == today and log.participant == current_user:
                today_habits.append(log.habit)
            elif log.date == yesterday and log.participant == current_user:
                yesterday_habits.append(log.habit)
            elif log.date == day_3 and log.participant == current_user:
                day_3_habits.append(log.habit)    
            elif log.date == day_4 and log.participant == current_user:
                day_4_habits.append(log.habit)
            elif log.date == day_5 and log.participant == current_user:
                day_5_habits.append(log.habit)
            elif log.date == day_6 and log.participant == current_user:
                day_6_habits.append(log.habit)
            elif log.date == day_7 and log.participant == current_user:
                day_7_habits.append(log.habit)
        
        context = {
            'current_user': current_user,
            'today': today,
            'yesterday': yesterday,
            'day_3': day_3,
            'day_4': day_4,
            'day_5': day_5,
            'day_6': day_6,
            'day_7': day_7,
            'participations': participations,
            'logs': logs,
            'users': users,
            'usernames': usernames,
            'habits': habits,
            'habits_of_user': habits_of_user,
            'today_habits': today_habits,
            'yesterday_habits': yesterday_habits,
            'day_3_habits': day_3_habits,
            'day_4_habits': day_4_habits,
            'day_5_habits': day_5_habits,
            'day_6_habits': day_6_habits,
            'day_7_habits': day_7_habits,
         }

        return render(request, "index.html", context)


def add_habit(request, name):
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if request.method == 'POST':

        current_user = request.user
        name = request.POST.get('name')
        current_user = request.user
        obj1 = Habit(name=name, creator=current_user)

        obj1.save()

        parti = Participation(participant=current_user, habit=obj1)
        parti.save()
        return redirect('home')

    return render(request, 'my_template.html')

def ekle_view(request):
    return render(request, 'ekle.html')

def habit_view(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    current_user = request.user
    context = {"habit": habit, "current_user": current_user}
    return render(request, 'habit.html', context)

def habit_done(request, habit_id, minus_day):
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if request.method == 'POST':
        current_user = request.user
        today = datetime.today() - timedelta(days=minus_day)
        
        try:
            obj = Log.objects.get(habit_id=habit_id, date=today, participant_id=current_user.id)
            obj.delete()
        except ObjectDoesNotExist:
            obj = Log(habit_id=habit_id, date=today, participant_id=current_user.id)
            obj.save()
            try:
                parti = Participation.objects.get(participant_id=current_user.id, habit_id=obj.habit_id)
            except ObjectDoesNotExist:
                parti = Participation(participant_id=current_user.id,habit_id=obj.habit_id)
                parti.save()

        return redirect('home')
    return render(request, 'my_template.html')

class Degistir(APIView):
    def post(self, request, name, habit_id):
        habit = Habit.objects.get(id=habit_id)
        if not request.user.is_authenticated:
            return HttpResponse("You are not authenticated. Please log in.")
        current_user = request.user
        if current_user.id == Habit.objects.get(id=habit_id).creator_id:

            name = request.POST.get('name')
            current_user = request.user

            obj = Habit.objects.get(id=habit_id)

            obj.name = name
            obj.save()
            return redirect('home')

        return redirect('home')
    
def sil(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if request.method == 'POST':
        current_user = request.user
        if current_user.id == Habit.objects.get(id=habit_id).creator_id or current_user.is_superuser:

            current_user = request.user
            # print(current_user.id)

            objs = Log.objects.filter(habit_id=habit_id)
            objs.delete()

            obj = Habit.objects.get(id=habit_id)
            obj.delete()

            objParti = Participation.objects.filter(habit_id=habit_id)
            objParti.delete()

            return redirect('home')


        return redirect('home')

    return render(request, 'my_template.html')

def arena_view(request):

    logs = Log.objects.all()

    today = datetime.today().date()
    yesterday = datetime.today().date() - timedelta(days=1)
    day_3 = datetime.today().date() - timedelta(days=2)
    day_4 = datetime.today().date() - timedelta(days=3)
    day_5 = datetime.today().date() - timedelta(days=4)
    day_6 = datetime.today().date() - timedelta(days=5)
    day_7 = datetime.today().date() - timedelta(days=6)

    current_user = request.user
    participations = Participation.objects.all()
    habits_of_user = []
    shared_habits_of_user = []

    day_7_habits = []
    day_6_habits = []
    day_5_habits = []
    day_4_habits = []
    day_3_habits = []
    yesterday_habits = []
    today_habits = []

    for log in logs:
        if log.date == today and log.participant:
            today_habits.append(log.habit)
        elif log.date == yesterday and log.participant:
            yesterday_habits.append(log.habit)
        elif log.date == day_3 and log.participant:
            day_3_habits.append(log.habit)    
        elif log.date == day_4 and log.participant:
            day_4_habits.append(log.habit)
        elif log.date == day_5 and log.participant:
            day_5_habits.append(log.habit)
        elif log.date == day_6 and log.participant:
            day_6_habits.append(log.habit)
        elif log.date == day_7 and log.participant:
            day_7_habits.append(log.habit) 

    for participation in participations:
        if participation.participant == current_user:
            habits_of_user.append(participation.habit)
    for habit in habits_of_user:
        for participation in participations:
            if participation.habit == habit and habit not in shared_habits_of_user and participation.participant != current_user:
                shared_habits_of_user.append(habit)
                continue




    shared_habits_of_user_len = len(shared_habits_of_user)
    
    users = User.objects.all()
    habits = Habit.objects.all()
    context = {
            'habits': habits,
            'users': users,
            'shared_habits_of_user_len': shared_habits_of_user_len,
            'today': today,
            'yesterday': yesterday,
            'day_3': day_3,
            'day_4': day_4,
            'day_5': day_5,
            'day_6': day_6,
            'day_7': day_7,
            'participations': participations,
            'logs': logs,
            'habits_of_user': habits_of_user,
            'today_habits': today_habits,
            'yesterday_habits': yesterday_habits,
            'day_3_habits': day_3_habits,
            'day_4_habits': day_4_habits,
            'day_5_habits': day_5_habits,
            'day_6_habits': day_6_habits,
            'day_7_habits': day_7_habits,
            'shared_habits_of_user': shared_habits_of_user,
            'current_user': current_user,
         }
    
    return render(request, 'arena.html', context)

def profile_view(request, user_id):
    current_user = request.user
    habits = Habit.objects.all()
    user = User.objects.get(id=user_id)
    participations = Participation.objects.all()
    context = {"user": user, "participations": participations, "habits": habits, "current_user": current_user, }
    return render(request, 'profile.html', context)

def katil(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if request.method == 'POST':
        current_user = request.user
        
        try:
            obj = Participation.objects.get(habit_id=habit_id, participant=current_user)
        except ObjectDoesNotExist:
            objParti = Participation(habit_id=habit_id, participant=current_user)
            objParti.save()
            
        

        return redirect('home')


    return redirect('home')

def ayril(request, habit_id):
    habit = Habit.objects.get(id=habit_id)
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if request.method == 'POST':
        current_user = request.user
        
        try:
            obj = Participation.objects.get(participant=current_user, habit_id=habit_id)
            obj.delete()
        except ObjectDoesNotExist:
            pass

        return redirect('home')


    return redirect('home')

def kullanici_sil(request, user_id):
    
    if not request.user.is_authenticated:
        return HttpResponse("You are not authenticated. Please log in.")
    if not request.user.is_superuser:
        return HttpResponse("You are not superuser")
    if request.method == 'POST':
        
        user_to_delete = User.objects.get(id=user_id)
        user_to_delete.delete()


        return redirect('home')

    return render(request, 'my_template.html')

    