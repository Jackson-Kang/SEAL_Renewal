
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^[a-zA-Zㄱ-힣0-9|s]*$', widget=forms.TextInput(dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(dict(required=True, max_length=30)), 
            label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(dict(required=True, max_length=30, 
                render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(dict(required=True, max_length=30, 
                render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.RegexField(required=False,regex=r'^[a-zA-Zㄱ-힣0-9|s]*$', 
        widget=forms.TextInput(attrs={'class' : 'form-control','max_length':30,'placeholder':"ID"}), label=("Hisnet ID"),
        error_messages={'invalid': _("알파벳, 한글, 숫자만 가능합니다.")})     
    password = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'class':'form-control','max_length' : 30,'render_value':False,'placeholder':'Password'}),label=("Password"))
    