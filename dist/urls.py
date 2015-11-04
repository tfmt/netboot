from django.conf.urls import url

from dist import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add$', views.AddCategoryView.as_view(), name='add_category'),
    url(r'^(?P<cat_id>\d+)/$', views.CategoryView.as_view(), name='category'),
]
