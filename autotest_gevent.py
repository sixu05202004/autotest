from gevent.wsgi import WSGIServer
from autotest.application import setup_app
app = setup_app()
http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()