from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

import re

ua_re = re.compile(r'^gPXE/(\d+).(\d+).(\d+)(\S*)'
                   '(?: \(netboot.me/(\d+).(\d+)(?:.(\d+))?\))?$')


class ViewMixin(object):
    def get_gpxe_versions(self):
        return self.parse_user_agent(self.request.META.get('User-Agent', ''))

    @property
    def is_gpxe(self):
        """
        Return whether the request comes from a gPXE instance.

        :return: bool
        """

        return self.request.META.get('User-Agent', '').startswith('gPXE')

    @staticmethod
    def parse_user_agent(ua):
        match = ua_re.match(ua)
        if not match:
            return (None, None, None, None), (None, None, None)
        else:
            groups = [int(x) if x and x.isdigit() else x for x in match.groups()]
            return tuple(groups[:4]), tuple(groups[4:])

    @staticmethod
    def redirect(url, resolve=True, *args, **kwargs):
        if resolve:
            url = reverse(url, *args, **kwargs)
        return HttpResponseRedirect(url)


class View(generic.View, ViewMixin):
    pass


class TemplateView(generic.TemplateView, ViewMixin):
    pass


# Regular views

class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if self.is_gpxe:
            return self.redirect('/menu.gpxe')
        return super(IndexView, self).dispatch(request, *args, **kwargs)


class MenuCfgView(View):
    pass


class MenuGpxeView(View):
    # Min version of ordinary gPXE that doesn't need upgrading
    MIN_GPXE_VER = (999, 0, 0) # All versions currently require upgrading

    # Min version of netboot.me gPXE that doesn't need upgrading
    MIN_NETBOOTME_VER = (0, 1, None)

    def get(self, request, *args, **kwargs):
        gpxe_ver, netboot_ver = self.get_gpxe_versions()

        if netboot_ver[0] is not None:
            if netboot_ver < self.MIN_NETBOOTME_VER:
                return self.upgrade()  # gPXE is too old
            else:
                return self.menu()
        elif gpxe_ver[0] is not None and gpxe_ver < self.MIN_GPXE_VER:
            return self.upgrade()  # regular gPXE is too old
        else:
            return self.menu()  # up-to-date version, or unrecognised UA

    @staticmethod
    def menu():
        response = HttpResponse(content_type='text/plain')
        response.write('#!gpxe\n')
        response.write('chain menu.c32 premenu.cfg\n')
        return response

    @staticmethod
    def upgrade():
        response = HttpResponse(content_type='text/plain')
        response.write('#!gpxe\n')
        response.write('echo\n')
        response.write(
            'echo Your copy of gPXE is too old. '
            'Upgrade at netboot.me to avoid seeing this every boot!\n')
        response.write('chain http://static.netboot.me/gpxe/netbootme.kpxe\n')
        return response
