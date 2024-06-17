from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import RegisterView, ResetPasswordView
from .forms import LoginForm

app_name = "app_auth"

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(template_name='app_auth/login.html', form_class=LoginForm, redirect_authenticated_user=True), name='signin'),
    path('logout/', LogoutView.as_view(template_name='app_auth/logout.html'), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='app_auth/password_reset_done.html'), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='app_auth/password_reset_confirm.html', success_url=reverse_lazy('app_auth:password_reset_complete')), name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='app_auth/password_reset_complete.html'), name='password_reset_complete'),
]