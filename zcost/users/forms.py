import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserChangeForm, UserCreationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label='Ваше имя пользователя (совпадает с номером телефона)',
                               widget=forms.TextInput(attrs={'data-phone-pattern': True}))

    def clean_username(self):
        username = self.cleaned_data['username']
        username = ''.join(re.findall(r'\d+', username))
        if len(username) != 11:
            msg = "Вы указали некорректное имя пользователя."
            self.add_error('username', msg)
            return None
        return username


class CreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='Ваше имя')
    last_name = forms.CharField(required=True, label='Ваша фамилия')
    email = forms.EmailField(required=True, label='Ваш Email')
    phone = forms.CharField(required=True, label='Ваш номер телефона',
                            widget=forms.TextInput(attrs={'data-phone-pattern': True}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')
        help_texts = {
            'username': 'Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'
        }

    def clean_phone(self):
        phone_str = self.cleaned_data['phone']
        phone_num = ''.join(re.findall(r'\d+', phone_str))
        if len(phone_num) != 11:
            msg = "Вы указали некорректный номер телефона."
            self.add_error('phone', msg)
            return None
        if User.objects.filter(username=phone_num).exists():
            msg = "Пользователь с данным телефоном уже существует."
            self.add_error('phone', msg)
            return None
        return phone_str

    def save(self, commit=True):
        user = super(CreationForm, self).save(commit=False)
        user.username = ''.join(re.findall(r'\d+', user.phone))
        if commit:
            user.save()
        return user


class PasswordResetFormValidation(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "Пользователь с данным адресом электронной почты не существует."
            self.add_error('email', msg)
        return email


class ChangeForm(UserChangeForm):
    first_name = forms.CharField(required=True, label='Ваше имя')
    last_name = forms.CharField(required=True, label='Ваша фамилия')
    email = forms.EmailField(required=True, label='Ваш Email')
    phone = forms.CharField(required=True, label='Ваш номер телефона',
                            widget=forms.TextInput(attrs={'data-phone-pattern': True}))
    password = None

    def clean_phone(self):
        phone_str = self.cleaned_data['phone']
        phone_num = ''.join(re.findall(r'\d+', phone_str))
        if len(phone_num) != 11:
            msg = "Вы указали неверный номер телефона."
            self.add_error('phone', msg)
            return None
        if User.objects.filter(username=phone_num).exists():
            msg = "Данный номер телефона уже привязан к другому пользователю."
            self.add_error('phone', msg)
            return None
        return phone_str

    def save(self, commit=True):
        user = super(ChangeForm, self).save(commit=False)
        user_phone = ''.join(re.findall(r'\d+', user.phone))
        if user.username == user_phone:
            return user
        user.username = user_phone
        user.save()
        return user

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')
