import logging

from flask import Flask, request, render_template
from livestatus import perform_query, perform_command
from livestatus_service import __version__ as livestatus_version

LOGGER = logging.getLogger("livestatus.webapp")

application = Flask(__name__)


def render_application_template(template_name, **template_parameters):
    template_parameters["version"] = livestatus_version
    return render_template(template_name, **template_parameters)


@application.route("/")
def handle_index():
    return render_application_template("index.html", **locals())


def dispatch_request(query, dispatch_function):
    query = query.replace('\\n', '\n')
    result = dispatch_function(query)
    return "{0}\n".format(result), 200


@application.route('/query', methods=['GET'])
def handle_query():
    query = request.args.get('q')
    return dispatch_request(query, perform_query)


@application.route('/cmd', methods=['GET'])
def handle_command():
    return dispatch_request(perform_command)
