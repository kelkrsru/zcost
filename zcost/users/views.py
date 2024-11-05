from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ChangeForm, CreationForm, LoginForm, PasswordResetFormValidation

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('accounts:signup_complete')
    template_name = 'users/signup.html'


def signup_complete(request):
    template = 'users/signup_complete.html'
    return render(request, template)


class ChangeUser(UpdateView):
    form_class = ChangeForm
    template_name = 'users/user_change.html'
    success_url = reverse_lazy('personal:index')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)


class Login(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('personal:index')
    redirect_authenticated_user = True


class Logout(auth_views.LogoutView):
    template_name = 'users/logout.html'


class PasswordReset(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    form_class = PasswordResetFormValidation


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetDone(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class PasswordChange(auth_views.PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')


class PasswordChangeDone(auth_views.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'
