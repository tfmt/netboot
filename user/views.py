from django.contrib.auth import authenticate, login, logout

from netboot.base_views import FormView, View

from user import forms


class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

        if user is not None:
            if not user.is_active:
                form.add_error('email', 'This user account is not activated.')
        else:
            form.add_error('email', 'Invalid login details.')

        if form.is_valid():
            return self.login(self.request, user)
        else:
            return self.form_invalid(form)

    @classmethod
    def login(cls, request, user):
        login(request, user)
        return cls.redirect('index')


class LogoutView(View):
    require_login = True

    def get(self, request, *args, **kwargs):
        logout(request)
        return self.redirect('index')
