from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from izppy.application import setup_app
app = setup_app()
http_server = HTTPServer(WSGIContainer(app))
http_server.listen(8080)
IOLoop.instance().start()