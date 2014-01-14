#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent.pywsgi import WSGIServer
from izppy.application import setup_app
app = setup_app()
http_server = WSGIServer(('', 8080), app)
http_server.serve_forever()