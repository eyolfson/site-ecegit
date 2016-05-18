from django import forms

class CommitTimeForm(forms.Form):
    term = forms.IntegerField(label="Term")
    timestamp = forms.DateTimeField(label="Timestamp")
