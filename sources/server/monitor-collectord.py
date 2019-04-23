#!/usr/bin/env python
import atexit
import datetime
import os
import sys
import time

from daemon import runner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modules.Models import Base, Server, Status
from modules.NginxStatus import NginxStatus


class MetricsCollector():
    def __init__(self, pid_file, poll_interval=60, db_path='/dev/shm/metrics.sqlite3', debug=True):
        self.stdin_path = '/dev/null'
        if debug:
            self.stdout_path = '/dev/tty'
            self.stderr_path = '/dev/tty'
            self.poll_interval = int(poll_interval/3)
        else:
            self.stdout_path = '/dev/null'
            self.stderr_path = '/dev/null'
            self.poll_interval = poll_interval
        self.pidfile_timeout = 5
        self.pidfile_path = pid_file
        self.db_path = db_path
        self.db_session = None
        self.server = None
        atexit.register(self.db_close)

    def run(self):
        # Initialise object to collect metrics
        nginx_status = NginxStatus()
        # Connect to database
        self.db_open(nginx_status.get_server_hostname())
        # First metrics poll to instantiate system information
        while True:
            # Poll and store
            dt = datetime.datetime.utcnow()
            data = nginx_status.poll_metrics()
            self.store_status(dt, data)
            time.sleep(self.poll_interval)

    def db_open(self, hostname='localhost'):
        engine = create_engine('sqlite:///'+self.db_path)
        Base.metadata.bind = engine
        Base.metadata.create_all(engine)
        DBSession = sessionmaker(bind=engine)
        self.db_session = DBSession()

        self.server = Server(hostname=hostname)
        self.db_session.add(self.server)
        self.db_session.commit()

    def db_close(self):
        if self.db_session:
            self.db_session.close()

    def db_rollback(self):
        self.db_session.rollback()

    def store_status(self, date_time, data):
        try:
            status = Status(active=data['active'],
                            reading=data['reading'],
                            writing=data['writing'],
                            waiting=data['waiting'],
                            timestamp=date_time.strftime('%s'),
                            server=self.server)
            self.db_session.add(status)
            self.db_session.commit()
        except Exception:
            print "Error accessing nginx status"
        finally:
            self.db_close()


def is_running(pid_file):
    try:
        with file(pid_file, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None
    except SystemExit:
        pid = None

    if pid:
        return True, pid
    else:
        return False, -1


# Main
SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
DB_FILE = SCRIPT_PATH + '/data/metrics.sqlite3'
PID_FILE = SCRIPT_PATH + '/.__PACKAGE_NAME__-collector.pid'
POLL_INTERVAL = 30
DEBUG = False

if __name__ == "__main__":
    if len(sys.argv) == 3:
        DEBUG = True
    if len(sys.argv) == 2:
        if 'status' == sys.argv[1]:
            running, pid = is_running(PID_FILE)
            if running:
                print '%s is running as pid %s' % (sys.argv[0], pid)
            else:
                print '%s is not running.' % sys.argv[0]
        elif 'stop' == sys.argv[1] and not is_running(PID_FILE)[0]:
            print '%s is not running.' % sys.argv[0]
        else:
            collector = MetricsCollector(PID_FILE, poll_interval=POLL_INTERVAL, db_path=DB_FILE, debug=DEBUG)
            daemon = runner.DaemonRunner(collector)
            daemon.do_action()  # start|stop|restart as sys.argv[1]
            running, pid = is_running(PID_FILE)
            sys.exit(0)
    else:
        print "Usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
else:
    print "%s can't be included in another program." % sys.argv[0]
    sys.exit(1)
