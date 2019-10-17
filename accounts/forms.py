from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile
from django.forms.widgets import DateInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    def clean_username(self):
        data = self.cleaned_data['username']
        if not data.islower():
            raise forms.ValidationError("Usernames should be in lowercase")
        return data
    class Meta:
       model = User
       fields = ['username','first_name','last_name','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length = 64)
    last_name = forms.CharField(max_length = 64)
    class Meta:
        model = User
        fields = ['first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices = (('M','Male'),('F','Female')))
    date_of_birth = forms.DateField(widget=forms.TextInput(     
        attrs={'type': 'date'} 
    ))#input_formats= ["%d-%m-%Y"])
    phone_number = forms.CharField(max_length = 15,label = "Mobile")
    phone_number1 = forms.CharField(max_length = 15,label = "Alternate mobile",required = False)
    bio = forms.CharField(max_length = 256,required = False,widget = forms.Textarea)
    website = forms.URLField(required = False)
    github = forms.URLField(required = False)
    linked_in = forms.URLField(required = False)
    class Meta:
        model = profile
        fields = ['gender','date_of_birth','phone_number','phone_number1','bio','website','github','linked_in']


