from django.conf.urls import url

from dist import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add$', views.AddCategoryView.as_view(), name='add_category'),
]
