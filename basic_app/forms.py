from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo,DeleteID,EditID,AddID,Poll,Choice,Vote,UserProperties
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm



class SearchForm(forms.Form):
    query = forms.CharField()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','email','password','first_name','last_name')
class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('bio','portfolio_site','profile_pic')
class UserPropertyForm(forms.ModelForm):
    class Meta():
        model = UserProperties
        fields = ('overall_ratings','work_balance_stars','culture_values_stars','career_opportunities_stars','company_benefit_stars','senior_management_stars')

class DeleteForm(forms.ModelForm):
    class Meta():
        model = DeleteID
        fields = ('did',)

class EditForm(forms.ModelForm):
    class Meta():
        model = EditID
        fields = ('eid','summary',)
class AddForm(forms.ModelForm):
    class Meta():
        model = AddID
        fields = ('cid','name','country','state','city',)

class PollForm(forms.ModelForm):
    choice1 = forms.CharField(
                        label='First Choice',
                        max_length=100,
                        min_length=1,
                        widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(
                        label='Second Choice',
                        max_length=100,
                        min_length=1,
                        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2']
        widgets = {
            'text': forms.Textarea(attrs={"class":"form-control", "rows": 5, "cols": 20})
        }

class EditPollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={"class":"form-control", "rows": 5, "cols": 20})
        }

class ChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ['choice_text']
