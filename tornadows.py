import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from tornado import httpserver, ioloop, wsgi, web

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--port', dest='port')

options, args = parser.parse_args()


def runserver():
    app_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(app_dir))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'problemotd.settings'
    django.setup()
    wsgi_app = wsgi.WSGIContainer(get_wsgi_application())
    application = web.Application([
        (r"/static/(.*)", web.StaticFileHandler, {"path": os.path.dirname(os.path.realpath(__file__)) + "/static"}),
        (r".*", web.FallbackHandler, dict(fallback=wsgi_app)),
    ])

    server = httpserver.HTTPServer(application)
    server.listen(options.port)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    runserver()
