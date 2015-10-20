from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic

import re

# Regex pattern to match PXE version
ua_re = re.compile(r'^([gi]PXE)/(\d+).(\d+).(\d+)(\S*)'
                   '(?: \(netboot.me/(\d+).(\d+)(?:.(\d+))?\))?$')


class GenericViewMixin(object):
    """
    A abstract mixin that implements additional methods for Views.
    """

    def detect_pxe(self):
        """
        Try to find out if the request comes from a compatible PXE.

        This method returns a tuple with PXE distribution, it's version
        and optionally the netboot.me version if found.
        If none of them can be detected, a 3-tuple of None is returned.

        :return: str or None
        """

        user_agent = self.request.META.get('HTTP_USER_AGENT', '')

        if user_agent:
            match = ua_re.match(user_agent)

            if match:
                groups = [int(x) if x and x.isdigit() else x for x in match.groups()[2:]]
                return groups[1], tuple(groups[:4]), tuple(groups[4:])

        return None, None, None

    def redirect(self, url, resolve=True, *args, **kwargs):
        """
        Returns a HTTP redirect response.

        :param url: URL
        :param resolve: Whether to resolve the url by using reverse()
        :param args: Resolve args
        :param kwargs: Resolve kwargs
        :return: HttpResponseRedirect
        """

        if resolve:
            url = reverse(url, *args, **kwargs)

        return HttpResponseRedirect(url)


class View(generic.View, GenericViewMixin):
    pass


class TemplateView(generic.TemplateView, GenericViewMixin):
    pass
