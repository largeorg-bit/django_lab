from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegisterForm


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object

        send_mail(
            subject="Добро пожаловать в SkyStore!",
            message=(
                f"Здравствуйте!\n\n"
                f"Вы успешно зарегистрировались в SkyStore.\n"
                f"Ваш логин: {user.email}\n\n"
                f"Спасибо, что выбрали наш сервис!"
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        messages.success(
            self.request,
            "Регистрация прошла успешно. Проверьте почту и войдите в аккаунт.",
        )
        return response


class UserLoginView(LoginView):
    """Авторизация пользователя по email и паролю."""

    form_class = UserLoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Выход из аккаунта."""

    next_page = reverse_lazy("home")
