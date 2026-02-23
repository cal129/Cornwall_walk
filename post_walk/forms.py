from django import forms
from .models import Comment
from .models import postwalk


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': 'Your Comment'
        }


class WalkForm(forms.ModelForm):
    class Meta:
        model = postwalk
        fields = ['title', 'location', 'description', 'distance', 'time_hours', 'time_minutes', 'difficulty', 'type', 'photo', 'coordinates']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Walk title'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Distance (km)'}),
            'time_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hours'}),
            'time_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minutes'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
           'coordinates': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Coordinates', 'value': '50.4155° N, 5.0737° W'}),
        }
