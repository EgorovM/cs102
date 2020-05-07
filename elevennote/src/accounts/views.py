from django.contrib.auth import authenticate, login
from django.views.generic import FormView

from .forms import UserCreationForm


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()

        email = self.request.POST['email']
        password = self.request.POST['password1']

        user = authenticate(email=email, password=password)
        login(self.request, user)

        return super(RegisterView, self).form_valid(form)


def confirm(request):
    code = request.GET.get('code', '')

    msg = "Error"

    if request.user.code == code:
        request.user.is_active = True
        request.user.save()
        msg = "You confirmed!"

    return redirect(f"notes/?msg={msg}")
