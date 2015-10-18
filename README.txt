This is netboot, a reimplementation of netboot.me with a modern code base.

netboot (aka netboot.me 2.0) is based on Django 1.8 (LTS) to be run with a WSGI
capable application server.  It's designed to run in combination with nginx.
The code is written with Python 3.5 and is optimised to be as fast as possible.

While netboot.me originally used Google App Engine with a pretty old Django
version and memcached to keep created configurations in memory, we'll generate
each user configuration on demand.

Implementation notes:

- It looks like netboot.me tries to detect gPXE (a customised gPXE version for
  netboot.me?) by user-agent string and redirects to /menu.gpxe right after.
