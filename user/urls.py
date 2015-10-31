from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^logout$', views.LogoutView.as_view(), name='logout'),
]
