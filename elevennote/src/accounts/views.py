from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import FormView
from django.shortcuts import redirect

from .forms import UserCreationForm

from django.core.mail import send_mail
import random
import string


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def send_email_confirmation(user):
    code = randomString(10)

    send_mail(
        "Confirm account",
        "",
        "yklab.noreply@yandex.ru",
        recipient_list=[user.email],
        html_message=f'<p>Hello {user.email}!</p><p>Please, confirm your email:)</p><a href="127.0.0.1:8000/accounts/confirm/{code}">Подтвердить аккаунт</a>',
        fail_silently=False,
    )

    return code


User = get_user_model()


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()

        email = self.request.POST['email']
        password = self.request.POST['password1']

        user = authenticate(email=email, password=password)

        code = send_email_confirmation(user)
        user.code = code

        user.save()

        login(self.request, user)

        return super(RegisterView, self).form_valid(form)


def confirm(request, code):
    msg = "Error"

    if request.user.code == code:
        request.user.is_active = True
        request.user.save()
        msg = "You confirmed!"

    return redirect(f"/notes/?msg={msg}")
