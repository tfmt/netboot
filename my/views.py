from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest

from netboot.base_views import TemplateView, View

from my.models import User
from my.oauth2 import google


class SigninView(TemplateView):
    template_name = 'my/signin.html'


class AuthView(View):
    URL_GET_TOKEN = 'https://accounts.google.com/o/oauth2/token'
    URL_PROFILE = 'https://www.googleapis.com/oauth2/v1/userinfo'

    @staticmethod
    def create_account(response):
        return User.objects.create_user(
            response['email'],
            None,
            is_active=True,
            google_id=response['id']
        )

    def get(self, request, *args, **kwargs):
        for key in ('state', 'code'):
            if not request.GET.get(key):
                return HttpResponseBadRequest('Missing parameter "%s"' % key)

        state = request.GET['state']
        code = request.GET['code']

        if state != request.session.get('gapi_state'):
            return HttpResponseBadRequest('Invalid state')

        google.redirect_uri = self.get_absolute_url(request, 'my:auth')

        try:
            google.fetch_token(
                self.URL_GET_TOKEN,
                code=code,
                client_secret=settings.GAPI_CLIENT_SECRET
            )
        except:
            messages.error(
                request,
                'An error has occured while performing sign in with Google. Please try again later.'
            )
            return self.redirect('my:signin')

        response = google.get(self.URL_PROFILE).json()

        if 'email' not in response or 'id' not in response:
            messages.error(request, 'Some fields were missing in the response. Please try again later.')
        elif not response.get('verified_email'):
            messages.error(
                request,
                'Your email address has not been verified with Google yet. Please verify and try again.')
        else:
            try:
                user = User.objects.get(google_id=response['id'])
            except User.DoesNotExist:
                user = self.create_account(response)

            if not messages.get_messages(request):
                self.signin(self.request, user)
                return self.redirect('index')

        return self.redirect('my:signin')

    def post(self, request, *args, **kwargs):
        google.redirect_uri = self.get_absolute_url(request, 'my:auth')

        authorization_url, state = google.authorization_url(
            'https://accounts.google.com/o/oauth2/auth',
            access_type='offline',
            approval_prompt='force')

        request.session['gapi_state'] = state

        return self.redirect(authorization_url, resolve=False)

    @staticmethod
    def signin(request, user):
        if not hasattr(user, 'backend'):
            user.backend = settings.AUTHENTICATION_BACKENDS[0]
        login(request, user)


class SignoutView(View):
    require_login = True

    def get(self, request, *args, **kwargs):
        logout(request)
        return self.redirect('index')
