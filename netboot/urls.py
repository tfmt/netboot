##
#  Copyright 2015 TFMT UG (haftungsbeschränkt).
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##

from django.conf.urls import include, url
from netboot import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^dist/', include('dist.urls', namespace='dist')),
    url(r'^menu\.cfg$', views.MenuCfgView.as_view(), name='menu_cfg'),
    url(r'^menu\.ipxe$', views.MenuIPXEView.as_view(), name='menu_ipxe'),
    url(r'^user/', include('user.urls', namespace='user')),
]
