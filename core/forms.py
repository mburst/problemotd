from django import forms
from core.models import ProblemSuggestion, Comment


class ProblemSuggestionForm(forms.ModelForm):
    class Meta:
        model = ProblemSuggestion
        fields = ['text']


class CommentForm(forms.ModelForm):
    ancestor = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'ancestor'}), required=False)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}))

    class Meta:
        model = Comment
        fields = ('name', 'website', 'text',)
