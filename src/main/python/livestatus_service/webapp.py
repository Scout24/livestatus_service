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


@application.route('/query', methods=['GET'])
def handle_query():
    query_command = request.args.get('q')
    query_command =  query_command.replace('\\n', '\n')
    query_result = perform_query(query_command)
    return ("{0}\n".format(query_result), 200)

@application.route('/cmd', methods=['GET'])
def handle_command():
    command = request.args.get('q')
    command =  command.replace('\\n', '\n')
    command_result = perform_command(command)
    return ("{0}\n".format(command_result), 200)
