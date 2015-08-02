import datetime
import calendar

from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

from userprofile.models import ProfessionalExperience ,UserProfile


class ProfessionalExperienceForm( ModelForm ):
    class Meta:
        model = ProfessionalExperience
        exclude = ('date_deleted', 'user')

    def clean(self):
        cleaned_data = super(ProfessionalExperienceForm, self).clean()
        return cleaned_data

    def save(self, *args, **kwargs):
        title =  self.cleaned_data['title']
        industries = self.cleaned_data['industry']
        description = self.cleaned_data['description']
        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']

        industries = industries.split(',')
        industries = [industry.strip() for industry in industries]

        try:
            user = User.objects.get(username = self.user)
        except User.DoesNotExist:
            return None

        pro_exp = ProfessionalExperience.objects.create(user = user, title = title, 
                                                        description = description, industry = industries,
                                                        date_from = date_from, date_to = date_to)

        return pro_exp


class UserProfileForm( forms.ModelForm ):

    class Meta:
        model = UserProfile
        exclude = ('score', 'user', 'summary', 'avatar', 'languages', 'awards', 'interests', 'date_deleted' ,'tags','address','phone','mobile','date_of_birth','email')
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        self.fields['country'].widget.attrs['class'] = 'span3'
        
        self.fields['city'].widget.attrs['class'] = 'span3'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
#        self.fields['city'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City'}))

        self.fields['website'].widget.attrs['class'] = 'span3'
        self.fields['website'].widget.attrs['placeholder'] = 'http://www.example.com'
#        self.fields['website'] = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'http://www.example.com'}))



