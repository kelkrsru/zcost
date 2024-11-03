from django.urls import path, re_path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('change-user/', views.ChangeUser.as_view(), name='change_user'),
    path('change-user/', views.ChangeUser.as_view(), name='change_user'),
    path('signup-complete/', views.signup_complete, name='signup_complete'),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('password-reset/', views.PasswordReset.as_view(), name="password_reset"),
    re_path(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path(r'password-reset-done/', views.PasswordResetDone.as_view(), name="password_reset_done"),
    path(r'password-reset-complete/', views.PasswordResetComplete.as_view(), name="password_reset_complete"),
    path('password-change/', views.PasswordChange.as_view(), name='password_change'),
    path('password-change-done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
]
