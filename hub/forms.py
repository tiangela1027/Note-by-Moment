from django import forms
from django.utils import timezone

class SubmitStamp(forms.Form):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"

    DEFAULT_MOODS = [
        (HAPPY, "Happy"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
    ]

    mood = forms.ChoiceField(choices=DEFAULT_MOODS)
    notes = forms.CharField(max_length=250, widget=forms.Textarea)
    title = forms.CharField(max_length=25)

class UpdateUserProfile(forms.Form):
    birthdate = forms.DateField(widget=forms.SelectDateWidget(
        years=range(timezone.now().date().year, timezone.now().date().year - 91, -1)
    ))

class GetUser(forms.Form):
    username = forms.CharField(max_length=25)
