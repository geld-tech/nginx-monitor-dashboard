#!/usr/bin/env python
"""
    Server Dashboard
    Display server resources usage
"""
import ConfigParser
import datetime
import logging
import logging.handlers
import sys
from optparse import OptionParser
from flask import Flask, render_template, jsonify

from modules.ServerMetrics import ServerMetrics
from modules.Models import Base, Server, SystemInformation, SystemStatus, Process

from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.debug = True

# Global config for API URLs and Tokens
config = ConfigParser.ConfigParser()
config.readfp(open('config/settings.cfg'))

# Initialisation
logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
logger = logging.getLogger('root')

server_metrics = ServerMetrics()

# DB Session
db_path = './data/metrics.sqlite3'
engine = create_engine('sqlite:///'+db_path)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/server", strict_slashes=False)
@app.route("/server/usage", strict_slashes=False)
def server_usage():
    try:
        now = datetime.datetime.utcnow()
        last_2_hours = now - datetime.timedelta(hours=24)
        data = {}

        hostname = server_metrics.get_server_hostname()
        server = db_session.query(Server).filter_by(hostname=hostname).first()

        data['hostname'] = hostname
        data['platform'] = server_metrics.get_server_platform()
        data['system'] = server_metrics.get_server_system()
        data['release'] = server_metrics.get_server_release()
        data['architecture'] = server_metrics.get_server_architecture()
        data['uptime'] = server_metrics.get_server_uptime()
        data['disks_usage'] = server_metrics.get_disks_usage()
        data['swap_usage'] = server_metrics.get_swapdisk_usage()

        sys_stat = db_session.query(SystemStatus).filter(func.DATE(SystemStatus.date_time) == now.date()).order_by(SystemStatus.id.desc()).first()
        if sys_stat:
            data['cpu_percent'] = sys_stat.cpu_percent
            data['vmem_percent'] = sys_stat.vmem_percent
            data['cpu_temp'] = sys_stat.cpu_temp

        processes_data = []
        for proc_status in db_session.query(Process).filter_by(server=server).order_by(Process.id):
            status = {}
            status['pid'] = proc_status.pid
            status['name'] = proc_status.name
            status['cpu_percent'] = proc_status.cpu_percent
            status['date_time'] = proc_status.date_time
            processes_data.append(status)
        data['processes'] = processes_data

        date_time_data = []
        cpu_percent_data = []
        vmem_percent_data = []
        swap_percent_data = []
        cpu_temp_data = []
        for sys_stat in db_session.query(SystemStatus).filter_by(server=server).filter(func.DATE(SystemStatus.date_time) >= last_2_hours).order_by(SystemStatus.id):
            date_time_data.append(sys_stat.date_time.strftime("%H:%M"))
            cpu_percent_data.append(sys_stat.cpu_percent)
            vmem_percent_data.append(sys_stat.vmem_percent)
            swap_percent_data.append(sys_stat.swap_percent)
            cpu_temp_data.append(sys_stat.cpu_temp)

        data['graphs_data'] = {'cpu_percent': cpu_percent_data,
                               'vmem_percent': vmem_percent_data,
                               'swap_percent': swap_percent_data,
                               'cpu_temp': cpu_temp_data,
                               'date_time': date_time_data}
        return jsonify({'data': data}), 200
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error('Error retrieving server resources usage: %s (line=%d)' % (e, exc_tb.tb_lineno))
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources usage, check logs for more details..'}), 500


@app.route("/server/information", strict_slashes=False)
def server_information():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for sys_info in db_session.query(SystemInformation).filter_by(server=server):
            status = {}
            status['platform'] = sys_info.platform
            status['system'] = sys_info.system
            status['release'] = sys_info.release
            data.append({server_metrics.get_server_hostname(): status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving server information: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.route("/processes/history", strict_slashes=False)
def processes_history():
    try:
        data = []
        server = db_session.query(Server).filter_by(hostname=server_metrics.get_server_hostname())[0]
        for proc_status in db_session.query(Process).filter_by(server=server):
            status = {}
            status['pid'] = proc_status.pid
            status['name'] = proc_status.name
            status['cpu_percent'] = proc_status.cpu_percent
            status['date_time'] = proc_status.date_time
            data.append({proc_status.name: status})
        return jsonify({'data': data}), 200
    except Exception, e:
        logger.error('Error retrieving processes history: %s' % e)
        return jsonify({'data': {}, 'error': 'Could not retrieve server resources status, check logs for more details..'}), 500


@app.route("/server/hostname")
def server_hostname():
    hostname = server_metrics.get_server_hostname()
    if hostname:
        return jsonify({'hostname': hostname}), 200
    else:
        return jsonify({"cpu_temp": "localhost", "error": "Couldn't read hostname, check logs for more details.."}), 500


@app.route("/nginx_status", strict_slashes=False)
def nginx_status():
    response = '''Active connections: 4
server accepts handled requests
1650 1650 9255
Reading: 0 Writing: 1 Waiting: 3'''
    return response, 200


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
