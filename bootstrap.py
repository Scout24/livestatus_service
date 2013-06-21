#!/usr/bin/env python

import sys
sys.path.append('src/main/python')
from livestatus_service.webapp import application
from livestatus_service import initialize

initialize("./livestatus.cfg")
application.debug = True
application.run(host='localhost', port=1337)
