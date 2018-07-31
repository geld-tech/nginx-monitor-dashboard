#!/usr/bin/env python
"""
    NGINX Status Stub
    Returns sample resources usage
"""
import logging
import logging.handlers
from optparse import OptionParser
from flask import Flask

app = Flask(__name__)
app.debug = True

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

@app.route("/")
@app.route("/nginx_status", strict_slashes=False)
def nginx_status():
    response = '''Active connections: 4
server accepts handled requests
1650 1650 9255
Reading: 0 Writing: 1 Waiting: 3'''
    return response, 200


if __name__ == "__main__":
    # Parse options
    opts_parser = OptionParser()
    opts_parser.add_option('--port', type="int", dest='port', help='IP Port to listen to.', default=8000)
    opts_parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = opts_parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0', port=options.port)
