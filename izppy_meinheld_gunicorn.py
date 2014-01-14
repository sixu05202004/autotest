#!/usr/bin/env python
# -*- coding: utf-8 -*-

import meinheld
from izppy.application import setup_app
app = setup_app()
meinheld.listen(('', 8080))
meinheld.run(app)
