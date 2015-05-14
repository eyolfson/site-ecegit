from django import forms

class CommitTimeForm(forms.Form):
    timestamp = forms.DateTimeField(label="Timestamp")
