from django import forms
from core.models import ProblemSuggestion, Comment


class ProblemSuggestionForm(forms.ModelForm):
    class Meta:
        model = ProblemSuggestion
        fields = ['text']


class CommentForm(forms.ModelForm):
    ancestor = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'ancestor'}), required=False)
    password = forms.CharField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '6'}), label="Comment")

    class Meta:
        model = Comment
        fields = ('name', 'text',)

    def is_valid(self):
        valid = super(CommentForm, self).is_valid()
        
        if not valid:
            return valid
        
        #Prevent spam bots without js
        if self.cleaned_data['password'] != 'potd':
            return False
        
        return True
    