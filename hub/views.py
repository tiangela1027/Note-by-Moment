from django.shortcuts import render, reverse, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from itertools import count
from functools import partial
from datetime import datetime, timedelta
from random import randint

from .models import Stamp, Profile
from .forms import SubmitStamp, UpdateUserProfile

feelings = {
    'HAPPY': 'happy',
    'SAD': 'sad',
    'ANGRY': 'angry',
}

# taken from https://www.codeofliving.com/blog/55-powerful-short-quotes-sayings-life/
quotes = [
    'Every moment is a fresh beginning. (T.S. Eliot)',
    'Never regret anything that made you smile. (Mark Twain)',
    'Die with memories, not dreams.',
    'What we think, we become. (Buddha)',
    'Be so good they can’t ignore you. (Steve Martin)',
    'Dream as if you’ll live forever, live as if you’ll die today. (James Dean)',
    'To live will be an awfully big adventure. (Peter Pan)',
    'Try to be a rainbow in someone’s cloud. (Maya Angelou)',
    'What consumes your mind controls your life.',
    'The meaning of life is to give life meaning. (Ken Hudgins)'
]

def filterHelper(user, mood):
    return Stamp.objects.filter(user=user, mood=mood)

def generateRandomQuote():
    return quotes[randint(0, 9)]

def getNumWeeksToToday(date):
    d2 = timezone.now().date()
    monday1 = (date - timedelta(days=date.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))
    return (monday2 - monday1).days / 7

class Feelings():
    def getFeelings():
        return feelings
        
    def addFeeling(feeling):
        feelings[feeling.upper()] = feeling.lower()

    def getPercentages(user, lst):
        percent_list = dict()
        total_size = len(lst)

        if total_size != 0:
            for feeling in feelings.values():
                size = len(lst.filter(user=user, mood=feeling))
                percent = round(size / total_size * 100)
                percent_list[feeling] = percent

        return percent_list

def getNotesForWeek(request, year, week):
    week = 52 * year + week + 1
    startDate = request.user.profile.birthdate + timedelta(weeks=week)
    endDate = request.user.profile.birthdate + timedelta(weeks=week + 1)

    stamps = Stamp.objects.filter(user=request.user, date__range=(startDate, endDate)).order_by('-date')

    paginator = Paginator(stamps, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_size = len(stamps)
    percent_list = Feelings.getPercentages(request.user, stamps)

    happy_list = filterHelper(request.user, "happy").filter(date__range=(startDate, endDate)).order_by('-date')
    sad_list = filterHelper(request.user, "sad").filter(date__range=(startDate, endDate)).order_by('-date')
    angry_list = filterHelper(request.user, "angry").filter(date__range=(startDate, endDate)).order_by('-date')

    context_dict = {
        'percent_list': percent_list,
        'size': total_size,
        'page_obj': page_obj,
        'happy': happy_list,
        'sad': sad_list,
        'angry': angry_list,
        'user': request.user,
        'stamps': stamps,
        'startDate': startDate,
        'endDate': endDate,
        'quote': generateRandomQuote(),
    }

    return render(request, 'hub/week.html', context_dict)

@login_required
def viewCollections(request):
    stamps = Stamp.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(stamps, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_size = len(stamps)
    percent_list = Feelings.getPercentages(
        request.user, 
        Stamp.objects.filter(user=request.user)
    )

    happy_list = filterHelper(request.user, "happy").order_by('-date')
    sad_list = filterHelper(request.user, "sad").order_by('-date')
    angry_list = filterHelper(request.user, "angry").order_by('-date')

    context_dict = {
        'percent_list': percent_list,
        'size': total_size,
        'page_obj': page_obj,
        'happy': happy_list,
        'sad': sad_list,
        'angry': angry_list,
        'user': request.user,
        'quote': generateRandomQuote(),
    }

    return render(request, 'hub/collections.html', context=context_dict)

def submitStamp(request):
    form = SubmitStamp()

    if request.method == "POST":
        form = SubmitStamp(request.POST)

        if form.is_valid():
            stamp = Stamp(
                user=request.user,
                mood=form.cleaned_data['mood'],
                notes=form.cleaned_data['notes'],
                title=form.cleaned_data['title'],
                date=timezone.now())
            stamp.save()
            form = SubmitStamp()
        else:
            form = SubmitStamp()

    return HttpResponseRedirect(reverse('hub:home'))

@login_required
def addStamp(request):
    total_size = len(Stamp.objects.filter(user=request.user))
    form = SubmitStamp()

    context_dict = {
        'form': form,
        'size': total_size,
        'user': request.user,
        'quote': generateRandomQuote(),
    }
    
    return render(request, 'hub/addstamp.html', context_dict)

@login_required
def userProfile(request):
    form = UpdateUserProfile()
    total_size = len(Stamp.objects.filter(user=request.user))

    context_dict = {
        'form': form,
        'size': total_size,
        'user': request.user,
        'quote': generateRandomQuote(),
    }

    return render(request, 'hub/userProfile.html', context_dict)

def updateUserProfile(request):
    form = UpdateUserProfile()

    if request.method == "POST":
        form = UpdateUserProfile(request.POST)

        if form.is_valid():
            birthdate = form.cleaned_data.get('birthdate')
            profile = Profile(request.user.id, birthdate)
            profile.save()
            request.user.profile = profile
            request.user.save()

    return HttpResponseRedirect(reverse('hub:home'))

@login_required
def calendar(request):
    total_size = len(Stamp.objects.filter(user=request.user))

    try:
        getNumWeeks = getNumWeeksToToday(request.user.profile.birthdate)
    except Profile.DoesNotExist:
        getNumWeeks = 0
     
    context_dict = {
        'size': total_size,
        'years': range(90),
        'weeks': range(52),
        'months': range(1, 13),
        'bound': getNumWeeks,
        'counter': partial(next, count()),
        'user': request.user,
        'quote': generateRandomQuote(),
    }
    return render(request, 'hub/calendar.html', context_dict)

@login_required
def updateCalendar(request):
    user = get_object_or_404(User, pk=request.POST['username'])
    return HttpResponseRedirect(reverse('hub:calendar'))
