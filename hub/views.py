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

from .models import Stamp, Profile
from .forms import SubmitStamp, UpdateUserProfile

feelings = {
    'HAPPY': 'happy',
    'SAD': 'sad',
    'ANGRY': 'angry',
}

def filterHelper(user, mood):
    return Stamp.objects.filter(user=user, mood=mood)

class Feelings():
    def getFeelings():
        return feelings
        
    def addFeeling(feeling):
        feelings[feeling.upper()] = feeling.lower()

    def getPercentages(user):
        percent_list = dict()
        total_size = len(Stamp.objects.filter(user=user))

        if total_size != 0:
            for feeling in feelings.values():
                size = len(filterHelper(user, feeling))
                percent = round(size / total_size * 100)
                percent_list[feeling] = percent

        return percent_list

@login_required
def viewCollections(request):
    stamps = Stamp.objects.filter(user=request.user)
    paginator = Paginator(stamps, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_size = len(stamps)
    percent_list = Feelings.getPercentages(request.user)

    happy_list = filterHelper(request.user, "happy")
    sad_list = filterHelper(request.user, "sad")
    angry_list = filterHelper(request.user, "angry")

    context_dict = {
        'percent_list': percent_list,
        'size': total_size,
        'page_obj': page_obj,
        'happy': happy_list,
        'sad': sad_list,
        'angry': angry_list,
        'user': request.user,
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

    return HttpResponseRedirect(reverse('hub:add'))

@login_required
def addStamp(request):
    total_size = len(Stamp.objects.filter(user=request.user))
    form = SubmitStamp()

    context_dict = {
        'form': form,
        'size': total_size,
        'user': request.user,
    }
    
    return render(request, 'hub/addstamp.html', context_dict)

def userProfile(request):
    form = UpdateUserProfile()
    total_size = len(Stamp.objects.filter(user=request.user))

    context_dict = {
        'form': form,
        'size': total_size,
        'user': request.user,
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

def getNumWeeksToToday(date):
    d2 = timezone.now().date()
    monday1 = (date - timedelta(days=date.weekday()))
    monday2 = (d2 - timedelta(days=d2.weekday()))
    return (monday2 - monday1).days / 7

@login_required
def calendar(request):
    total_size = len(Stamp.objects.filter(user=request.user))
    getNumWeeks = getNumWeeksToToday(request.user.profile.birthdate)
    context_dict = {
        'size': total_size,
        'years': range(90),
        'weeks': range(52),
        'bound': getNumWeeks,
        'counter': partial(next, count()),
        'user': request.user
    }
    return render(request, 'hub/calendar.html', context_dict)

@login_required
def updateCalendar(request):
    user = get_object_or_404(User, pk=request.POST['username'])
    return HttpResponseRedirect(reverse('hub:calendar'))
