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

from django.http import HttpResponse

from netboot.base_views import TemplateView, View


class IndexView(TemplateView):
    """
    Index view.

    This will redirect to the PXE menu in case a valid PXE
    environment has been detected. Otherwise, it displays
    our home page.
    """

    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        pxe_ver = self.detect_pxe()
        if pxe_ver:
            return self.redirect('menu_ipxe')
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class MenuCfgView(View):
    pass


class MenuIPXEView(View):
    def get(self, request, *args, **kwargs):
        pxe_ver = self.detect_pxe()

        if pxe_ver:
            return self.menu()
        else:
            return self.upgrade()

    @staticmethod
    def menu():
        menu = [
            '#!ipxe',
            'chain menu.c32 premenu.cfg',
            ''
        ]

        response = HttpResponse(content_type='text/plain')
        response.write('\n'.join(menu))
        return response

    @staticmethod
    def upgrade():
        output = [
            '#!ipxe',
            'echo'
            'echo Your copy of the PXE software is too old. '
            'Upgrade at netboot.me to avoid seeing this every boot.',
            'chain http://static.netboot.me/gpxe/netbootme.kpxe',
            ''
        ]

        response = HttpResponse(content_type='text/plain')
        response.write('\n'.join(output))
        return response
