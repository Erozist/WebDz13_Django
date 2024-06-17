from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import RegisterForm

class RegisterView(View):
    template_name = 'app_auth/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:quotes-list")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо {username}. Ваш акаунт успішно створено")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})


# def profile(request):
#     # if request.method == 'POST':
#     #     profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#     #     if profile_form.is_valid():
#     #         profile_form.save()
#     #         messages.success(request, 'Your profile is updated successfully')
#     #         return redirect(to='users:profile')

#     # profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'users/profile.html', {'profile_form': profile_form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app_auth/password_reset.html'
    email_template_name = 'app_auth/password_reset_email.html'
    html_email_template_name = 'app_auth/password_reset_email.html'
    success_url = reverse_lazy('app_auth:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'app_auth/password_reset_subject.txt'
