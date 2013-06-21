import logging

from flask import Flask, request, render_template
from livestatus import perform_query, perform_command
from livestatus_service import __version__ as livestatus_version
import traceback


LOGGER = logging.getLogger('livestatus.webapp')

application = Flask(__name__)


def render_application_template(template_name, **template_parameters):
    template_parameters['version'] = livestatus_version
    return render_template(template_name, **template_parameters)


@application.route('/')
def handle_index():
    return render_application_template('index.html', **locals())


@application.route('/query', methods=['GET'])
def handle_query():
    return validate_and_dispatch(request, perform_query)


@application.route('/cmd', methods=['GET'])
def handle_command():
    return validate_and_dispatch(request, perform_command)


def dispatch_request(query, dispatch_function, **kwargs):
    result = dispatch_function(query, **kwargs)
    return '{0}\n'.format(result), 200


def validate_query(query):
    if not query:
        raise ValueError('The "q" parameter (query) is mandatory.')
    query = query.replace('\\n', '\n')
    return query


def validate_and_dispatch(request, dispatch_function):
    try:
        query = request.args.get('q')
        query = validate_query(query)
        key = request.args.get('key')
        return dispatch_request(query, dispatch_function, key=key)
    except BaseException, exception:
        LOGGER.error(traceback.format_exc())
        return 'Error : %s' % exception, 500
