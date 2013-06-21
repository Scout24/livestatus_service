from livestatus_service.webapp import application, initialize

initialize('/etc/livestatus.cfg')
application.debug = False
