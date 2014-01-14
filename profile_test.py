#!/usr/bin/env python
# -*- coding: utf-8 -*-

from izppy.application import setup_app
from werkzeug.contrib.profiler import ProfilerMiddleware

"""Just for test!!!"""

app = setup_app()
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
app.run(host='0.0.0.0',debug = True)