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

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views import generic

import re

# Regex pattern to match iPXE version
ua_re = re.compile(r'^iPXE/(\d+).(\d+).(\d+)(\S*)')


class GenericViewMixin(object):
    """
    An abstract mixin that implements additional methods for views.
    """

    require_login = False
    require_admin = False

    def detect_pxe(self):
        """
        Try to find out if the request comes from an iPXE instance.

        :return: str or None
        """

        user_agent = self.request.META.get('HTTP_USER_AGENT', '')

        if user_agent:
            match = ua_re.match(user_agent)

            if match:
                return [int(x) if x and x.isdigit() else x for x in match.groups()]

        return None

    def dispatch(self, request, *args, **kwargs):
        if (self.require_login or self.require_admin) and not request.user.is_authenticated():
            return HttpResponseForbidden()
        elif self.require_admin and not request.user.is_admin:
            return HttpResponseForbidden()

        return super(GenericViewMixin, self).dispatch(request, *args, **kwargs)

    @staticmethod
    def get_absolute_url(request, path, resolve=True, *args, **kwargs):
        """
        Build absolute URL by taking current HTTP host and path together.

        :param request: HttpRequest
        :param path: Path to append
        :param resolve: Whether to resolve path to URL
        :param args: Arguments
        :param kwargs: Keyword arguments
        :return: str
        """
        scheme = 'https' if request.is_secure() else 'http'
        host = request.get_host()

        if resolve:
            path = reverse(path, *args, **kwargs)

        return '{scheme}://{host}{path}'.format(scheme=scheme, host=host, path=path)

    @staticmethod
    def redirect(url, resolve=True, *args, **kwargs):
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


class View(GenericViewMixin, generic.View):
    pass


class TemplateView(GenericViewMixin, generic.TemplateView):
    pass


class FormView(GenericViewMixin, generic.FormView):
    pass
