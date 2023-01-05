from django import forms
from .models import *

# Music add form
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ('name', 'singer', 'genre', 'album', 'description', 'release_date', 'image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("comment", "rating")
