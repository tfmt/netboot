from django.conf.urls import url

from my import views

urlpatterns = [
    url(r'^auth$', views.AuthView.as_view(), name='auth'),
    url(r'^signin$', views.SigninView.as_view(), name='signin'),
    url(r'^signout$', views.SignoutView.as_view(), name='signout'),
]
