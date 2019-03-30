from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'referral_code',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'validate'
            })

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')
        code = str(referral_code)
        if referral_code is not None:
            all_referrals = Referral.objects.all()
            last_added_id = 0
            work = False
            for all_referrals in Referral.objects.all():
                last_added_id = all_referrals.id
            for i in range(last_added_id):
                referrals_exists = Referral.objects.filter(id=i+1).exists()
                if referrals_exists :
                    referral = Referral.objects.get(id=i+1)
                    if referral.referral_code == code:
                        work = True
                        break
            if work == False:
                raise forms.ValidationError(u'Invalid Referral Code !')
        return referral_code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'A user with that email address already exists.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        f_name = str(first_name)
        leng = len(f_name)
        if leng == 0:
            raise forms.ValidationError(u'Enter the first name.')
        return first_name

    # def clean_last_name(self):
    #     last_name = self.cleaned_data.get('last_name')
    #     f_name = str(last_name)
    #     leng = len(f_name)
    #     if leng == 0:
    #         raise forms.ValidationError(u'Enter the last name.')
    #     return last_name


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(min_length=100, max_length=5000, label='Add a bio',
                          widget=forms.Textarea(attrs={'class': 'materialize-textarea', 'data-length': '5000'}))

    class Meta:
        model = User
        fields = ('bio',)


class CasualForm(forms.ModelForm):

    class Meta:
        model = Casual
        fields = '__all__'
        
class IntermediateForm(forms.ModelForm):

    class Meta:
        model = Intermediate
        fields = '__all__'


class ExtremeForm(forms.ModelForm):

    class Meta:
        model = Extreme
        fields = '__all__'