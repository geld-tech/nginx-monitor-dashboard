#!/usr/bin/env python
"""
    Server Dashboard
    Display server resources usage
"""
import ConfigParser
import logging
import logging.handlers
from optparse import OptionParser
from flask import Flask, render_template, jsonify

from modules.NginxStatus import NginxStatus
from modules.Models import Base, Server, Status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

nginx_status = NginxStatus()

# DB Session
db_path = './data/metrics.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/nginx_status", strict_slashes=False)
def status():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=nginx_status.get_server_hostname())[0]
        result = db_session.query(Status).filter_by(server=server)[0]
        status = {}
        status['active'] = result.active
        status['reading'] = result.reading
        status['writing'] = result.writing
        status['waiting'] = result.waiting
        data.append(status)
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving nginx status: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve nginx status, check logs for more details..'}), 500


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"data": "not found", "error": "resource not found"}), 404


if __name__ == "__main__":
    # Parse options
    opts_parser = OptionParser()
    opts_parser.add_option('--debug', action='store_true', dest='debug', help='Print verbose output.', default=False)
    options, args = opts_parser.parse_args()
    if options.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Enabled DEBUG logging level.')
    logger.info('Options parsed')
    app.run(host='0.0.0.0')
