from pybuilder.core import init, use_plugin, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.coverage")
use_plugin("python.pydev")
use_plugin("python.distutils")
use_plugin('copy_resources')
use_plugin('python.flake8')

use_plugin("python.install_dependencies")

default_task = ["analyze", "publish"]

name = "livestatus-service"
version = "0.1.2"
description = "Livestatus-service is a WSGI application that exposes the functionality of a livestatus \
socket to the outside world over HTTP. \nQuery results are formatted to be more machine readable and it \
is also possible to send commands over the livestatus socket or using the nagios/icinga command file."
summary = "Exposes MK livestatus to the outside world over HTTP"
authors = (Author("Marcel Wolf", "marcel.wolf@immobilienscout24.de"),
           Author("Maximilien Riehl", "maximilien.riehl@gmail.com"))
url = "https://github.com/mriehl/livestatus-service"
license = "WTFPL"


@init
def initialize(project):
    project.port_to_run_on = "8080"


    project.build_depends_on("mockito")
    project.build_depends_on("mock")


    project.depends_on("flask")


    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.get_property("filter_resources_glob").append("**/livestatus_service/__init__.py")
    project.get_property("filter_resources_glob").append("**/livestatus_service/livestatus_service.conf")


    project.install_file('/var/www', 'livestatus_service/livestatus_service.wsgi')
    project.install_file('/etc/httpd/conf.d/', 'livestatus_service/livestatus_service.conf')

    project.include_file("livestatus_service", "templates/*.html")
    project.set_property("coverage_threshold_warn", 85)
    project.set_property("coverage_break_build", False)


    project.set_property('distutils_classifiers', [
      'Development Status :: 4 - Beta',
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'Intended Audience :: System Administrators',
      'Programming Language :: Python',
      'Natural Language :: English',
      'Operating System :: POSIX :: Linux',
      'Topic :: System :: Monitoring'])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')
