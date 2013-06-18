import sys
sys.path.append('src/main/python')
from livestatus_service.webapp import application
from livestatus_service import initialize

initialize("./livestatus.cfg")
application.debug=True
import socket
application.run(host=socket.getfqdn(), port=1337)
