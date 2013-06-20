livestatus-service
==================

## Background
Icinga is a pretty cool monitoring solution (especially when compared to a monolithic dinosaur like nagios)
but unfortunately it lacks any means of remote-control which is a sine-qua-none requirement for deployment automation.
The most obvious use case is scheduling downtimes programatically.

MK-Livestatus is a Nagios/Icinga extension that allows queries and commands by accessing an UNIX socket on the machine.
An added benefit is that queries always return up-to-date information as opposed to the ominous global state file 
(searching for "status.dat" should get you going on this). Unfortunately having a local socket also means that accessing
livestatus over the network is not possible out-of-the-box.

Livestatus-service solves this problem by exposing the full functionality of the socket over a simple HTTP API.


## 1-step checkout, test, build
```bash
sudo pip install pyb-init && pyb-init github mriehl : livestatus_service
```

Afterwards, building and packaging can be done with
```bash
source venv/bin/activate
pyb
cd target/dist/livestatus-service-$VERSION
python setup.py bdist_rpm
```

## Running
```bash
source venv/bin/activate
python bootstrap.py
```

## Deploying
Build a software package.

The application will try to run as WSGI behind a httpd webserver by including configuration in ```/etc/httpd/conf.d/```.
Building an RPM will work out-of-the-box with ```setup.py bdist_rpm```, other packages should be easy to build too.
The application should work out-of-the-box.

## Configuration
### Application configuration
See [the example config file](https://github.com/mriehl/livestatus_service/blob/master/livestatus.cfg).
Configuration should be in /etc/livestatus.cfg
### Webserver configuration
By default the service will want to run on port 8080 but you can change this by modifying [the build configuration](https://github.com/mriehl/livestatus_service/blob/master/build.py)
before building.
Changing the value of ```project.port_to_run_on = "8080"``` will ensure that pybuilder patches in the correct port in the httpd configuration files. 

