'''
The MIT License (MIT)

Copyright (c) 2013 ImmobilienScout24

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from pybuilder.core import init, use_plugin, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.coverage")
use_plugin("python.distutils")
use_plugin('copy_resources')
use_plugin('python.flake8')

use_plugin("python.install_dependencies")

default_task = ["analyze", "publish"]

name = "livestatus-service"
version = "0.3.5"
summary = "Exposes MK livestatus to the outside world over HTTP"
authors = (Author("Marcel Wolf", "marcel.wolf@immobilienscout24.de"),
           Author("Maximilien Riehl", "maximilien.riehl@immobilienscout24.de"))
url = "https://github.com/ImmobilienScout24/livestatus_service"
license = "MIT"


@init
def initialize(project):
    project.port_to_run_on = "8080"

    project.build_depends_on("mock")

    project.depends_on("flask")
    project.depends_on("simplejson")

    project.set_property("verbose", True)

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')
    project.get_property('copy_resources_glob').append('README')

    project.set_property('flake8_include_test_sources', True)
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_ignore', "E501,E731")

    project.get_property("filter_resources_glob").append("**/livestatus_service/__init__.py")
    project.get_property("filter_resources_glob").append("**/livestatus_service/livestatus_service.conf")

    project.install_file('/var/www', 'livestatus_service/livestatus_service.wsgi')
    project.install_file('/etc/httpd/conf.d/', 'livestatus_service/livestatus_service.conf')

    project.include_file("livestatus_service", "templates/*.html")
    project.set_property("coverage_threshold_warn", 99)
    project.set_property("coverage_break_build", True)

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: Jython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package', 'verify']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')
    project.set_property('teamcity_output', True)
