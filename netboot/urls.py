from django.conf.urls import include, url
from netboot import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^menu\.cfg$', views.MenuCfgView.as_view()),
    url(r'^menu\.gpxe$', views.MenuGpxeView.as_view()),
]
