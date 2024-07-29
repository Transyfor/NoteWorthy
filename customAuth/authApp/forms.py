from django import forms
from .models import MyUser
passwordInputWidget = {
 'password': forms.PasswordInput(),
}
class RegisterForm(forms.ModelForm):
 class Meta:
  model = MyUser
  fields = '__all__'
  widgets = [passwordInputWidget]

class LoginForm(forms.ModelForm):
 class Meta:
  model = MyUser
  fields = ['username', 'password']
  widgets = [passwordInputWidget]