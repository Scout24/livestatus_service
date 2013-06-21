from livestatus_service.webapp import application
from livestatus_service import initialize

initialize('/etc/livestatus.cfg')
application.debug = False
