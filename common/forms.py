from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'bio', 'email', 'avatar')

