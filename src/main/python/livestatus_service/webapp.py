import logging

from flask import Flask, request
from livestatus import perform_query, perform_command

LOGGER = logging.getLogger("livestatus.webapp")

application = Flask(__name__)

@application.route("/")
def handle_index():
    return ('todo', 200)


@application.route('/query', methods=['GET'])
def handle_query():
    query_command = request.args.get('q')
    query_command =  query_command.replace('\\n', '\n')
    query_result = perform_query(query_command)
    LOGGER.debug('Query {0} had result {1}'.format(query_command, query_result))
    return ("{0}\n".format(query_result), 200)

@application.route('/cmd', methods=['GET'])
def handle_command():
    command = request.args.get('q')
    command =  command.replace('\\n', '\n')
    command_result = perform_command(command)
    LOGGER.debug('Command {0} had result {1}'.format(command, command_result))
    return ("{0}\n".format(command_result), 200)
