#!/usr/bin/env python
import atexit
from daemon import runner
import datetime
import sys
import time
from modules.ServerMetrics import ServerMetrics
from modules.Models import Base, Server, SystemInformation, SystemStatus, Process
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MetricsCollector():
    def __init__(self, pid_file, poll_interval=30, db_path='/dev/shm/monitor-collectord.sqlite3'):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_timeout = 5
        self.pidfile_path = pid_file
        self.poll_interval = poll_interval
        self.db_path = db_path
        self.db_session = None
        self.server = None
        atexit.register(self.db_close)

    def run(self):
        # Initialise object to collect metrics
        sm = ServerMetrics()
        hostname = sm.get_server_hostname()
        # Connect to database
        self.db_open(hostname)
        # First metrics poll to instantiate system information
        data = sm.poll_metrics()
        self.store_system_information(data)
        while True:
            # Poll and store
            ts = datetime.datetime.utcnow()
            data = sm.poll_metrics()
            self.store_system_status(ts, data)
            self.store_processes(ts, data)
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

    def store_system_information(self, data):
        sys_info = SystemInformation(platform=data['platform'],
                                     system=data['system'],
                                     release=data['release'],
                                     server=self.server)
        self.db_session.add(sys_info)
        self.db_session.commit()

    def store_system_status(self, timestamp, data):
        sys_status = SystemStatus(cpu_percent=data['cpu_percent'],
                                  vmem_percent=data['vmem_percent'],
                                  cpu_temp=data['cpu_temp'],
                                  swap_percent=data['swap_usage']['percent'],
                                  date_time=timestamp,
                                  server=self.server)
        self.db_session.add(sys_status)
        self.db_session.commit()

    def store_processes(self, timestamp, data):
        for proc in data['processes']:
            if proc['cpu_percent'] > 0.9:  # Won't store irrelevant information
                process = Process(pid=proc['pid'],
                                  name=proc['name'],
                                  cpu_percent=proc['cpu_percent'],
                                  date_time=timestamp,
                                  server=self.server)
                self.db_session.add(process)
                self.db_session.commit()


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
PID_FILE = '/tmp/monitor-collectord.pid'
POLL_INTERVAL = 15

if __name__ == "__main__":
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
            collector = MetricsCollector(PID_FILE, poll_interval=POLL_INTERVAL)
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
