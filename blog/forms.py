from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField()


class CustomLoginForm(AuthenticationForm):
    age = forms.IntegerField(label="Age", required=True)

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 12:
            raise ValidationError("You must be at least 12 years old to sign in.")
        return age
