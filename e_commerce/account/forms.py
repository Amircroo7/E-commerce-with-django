from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'phone_number',  'full_name']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password dont match')
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user
    
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=" you can change password using  <a href=\" ../password/\">this form</a>"
    )
    class Meta:
        model = User
        fields = ['email', 'phone_number',  'full_name', 'password']
        
        
class UserRegistrationForm(forms.Form):
    phone = forms.CharField(max_length=11)
    email = forms.CharField()
    full_name = forms.CharField(label='Full Name')
    password = forms.CharField(widget=forms.PasswordInput)
    
class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label='Code')
    
    