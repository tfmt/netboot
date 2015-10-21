This is netboot, a reimplementation of netboot.me with a modern code base.

netboot (aka netboot.me 2.0) is based on Django 1.8 (LTS) to be run with a WSGI
capable application server.  It's designed to run in combination with nginx.
The code is written with Python 3.5 and is optimised for performance.

While netboot.me originally used Google App Engine with a pretty old Django
version and memcached to keep created configurations in memory, we'll generate
each user configuration on demand.

netboot.me was created by Nick Johnson and is now maintained by TFMT UG.
