from django.conf import settings

from requests_oauthlib import OAuth2Session

scope = ['https://www.googleapis.com/auth/userinfo.email']
google = OAuth2Session(settings.GAPI_CLIENT_ID, scope=scope)
