#!/usr/bin/env python
"""
    Server Metrics for Resources and Usage
"""
import logging
import logging.handlers
import os
import platform
import psutil
import time
import socket


class ServerMetrics:
    def __init__(self):
        logging.basicConfig(format='[%(asctime)-15s] [%(threadName)s] %(levelname)s %(message)s', level=logging.INFO)
        self.logger = logging.getLogger('root')
        self._data = {}
        self.hostname = self._get_server_hostname()
        self.collect_metrics()

    def get(self):
        return self._data

    def poll_metrics(self):
        self.collect_metrics()
        return self._data

    def collect_metrics(self):
        self._data = self._get_metrics()

    def _get_metrics(self):
        try:
            server_platform = self.get_server_platform()
            server_system = self.get_server_system()
            server_release = self.get_server_release()
            server_architecture = self.get_server_architecture()
            uptime = self.get_server_uptime()
            cpu_temp = self.get_server_temperature()
            cpu_percent = self.get_server_cpu_percent()
            mem_percent = self.get_server_memory_percent()
            vmem_percent = self.get_server_virtual_memory_percent()
            processes = self.get_server_processes()
            processes_status = self.get_server_processes_status()
            disks_usage = self.get_disks_usage()
            disks_io = self.get_disks_io()
            swap_usage = self.get_swapdisk_usage()
            network_io = self.get_network_io()  # Requires to poll during interval to get rate
            data = {'hostname': self.get_server_hostname(),
                    'platform': server_platform,
                    'system': server_system,
                    'release': server_release,
                    'architecture': server_architecture,
                    'uptime': uptime,
                    'cpu_temp': cpu_temp,
                    'cpu_percent': cpu_percent,
                    'mem_percent': mem_percent,
                    'vmem_percent': vmem_percent,
                    'processes': processes,
                    'processes_status': processes_status,
                    'disks_usage': disks_usage,
                    'disks_io': disks_io,
                    'swap_usage': swap_usage,
                    'network_io': network_io}
            return data
        except Exception, e:
            self.logger.error('Error retrieving server metrics: %s' % e)
            return {}

    def get_server_temperature(self):
        try:
            if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
                with open('/sys/class/thermal/thermal_zone0/temp') as temp_file:
                    cpu_temp = int(temp_file.read()) / 1000
            else:
                return -273
            return cpu_temp
        except Exception, e:
            self.logger.error('Error reading temperature: %s' % e)
            return False

    def _get_server_hostname(self):
        try:
            hostname = socket.gethostname()
            return hostname
        except Exception, e:
            self.logger.error('Error reading hostname: %s' % e)
            return False

    def get_server_hostname(self):
        return self.hostname

    def get_server_platform(self):
        try:
            return platform.platform()
        except Exception, e:
            self.logger.error('Error reading plaftorm: %s' % e)
            return False

    def get_server_system(self):
        try:
            return platform.system()
        except Exception, e:
            self.logger.error('Error reading operating system: %s' % e)
            return False

    def get_server_architecture(self):
        try:
            return platform.machine()
        except Exception, e:
            self.logger.error('Error reading machine architecture: %s' % e)
            return False

    def get_server_release(self):
        try:
            return platform.release()
        except Exception, e:
            self.logger.error('Error reading release: %s' % e)
            return False

    def get_server_uptime(self):
        try:
            uptime = time.time() - psutil.boot_time()
            return uptime
        except Exception, e:
            self.logger.error('Error reading uptime: %s' % e)
            return False

    def get_server_cpu_percent(self):
        try:
            psutil.cpu_percent(interval=1)
            time.sleep(0.1)
            return psutil.cpu_percent(interval=0)
        except Exception, e:
            self.logger.error('Error reading CPU percentage: %s' % e)
            return False

    def get_server_virtual_memory_percent(self):
        try:
            return psutil.virtual_memory().percent
        except Exception, e:
            self.logger.error('Error reading Virtual Memory percentage: %s' % e)
            return False

    def get_server_disk_usage_percent(self, mountpoint='/'):
        try:
            return psutil.disk_usage(mountpoint).percent
        except Exception, e:
            self.logger.error('Error reading Disk Usage Mountpoint percentage: %s' % e)
            return False

    def get_server_processors_count(self):
        try:
            return psutil.cpu_count()
        except Exception, e:
            self.logger.error('Error reading count of CPU: %s' % e)
            return False

    def get_server_memory_percent(self):
        try:
            os_proc = psutil.Process(os.getpid())
            mem_percent = os_proc.memory_info()[0] / float(2 ** 20)
            return mem_percent
        except Exception, e:
            self.logger.error('Error reading Memory percentage: %s' % e)
            return False

    def get_server_processes(self):
        try:
            processes = []
            for proc in psutil.process_iter():
                if proc.pid > 1:
                    process = {'pid': proc.pid, 'name': proc.name(), 'cpu_percent': proc.cpu_percent()}
                    processes.append(process)
            sorted_processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:12]
            return sorted_processes
        except Exception, e:
            self.logger.error('Error retrieving processes: %s' % e)
            return False

    def get_server_processes_status(self):
        try:
            processes_status = {'running': 0,
                                'paused': 0,
                                'start_pending': 0,
                                'pause_pending': 0,
                                'continue_pending': 0,
                                'stop_pending': 0,
                                'stopped': 0}
            for p in psutil.process_iter():
                try:
                    p.dict = p.as_dict()
                    try:
                        processes_status[p.dict['status']] += 1
                    except KeyError:
                        processes_status[p.dict['status']] = 1
                except psutil.NoSuchProcess:
                    pass
            return processes_status
        except Exception, e:
            self.logger.error('Error retrieving processes status: %s' % e)
            return False

    def get_server_processes_with_memory(self, max_count=12):
        try:
            properties = ['username', 'nice', 'memory_info', 'memory_percent', 'cpu_percent', 'cpu_times', 'name', 'status']
            procs_status = {'running': 0, 'paused': 0, 'start_pending': 0, 'pause_pending': 0, 'continue_pending': 0, 'stop_pending': 0, 'stopped': 0}
            processes = []
            for p in psutil.process_iter():
                try:
                    p.dict = p.as_dict(properties)
                    try:
                        procs_status[p.dict['status']] += 1
                    except KeyError:
                        procs_status[p.dict['status']] = 1
                except psutil.NoSuchProcess:
                    pass
                else:
                    processes.append(p)
            sorted_processes = sorted(processes, key=lambda p: p.dict['cpu_percent'], reverse=True)
            return (sorted_processes, procs_status)  # return processes sorted by CPU and stats
        except Exception, e:
            self.logger.error('Error retrieving processes: %s' % e)
            return False

    def get_disks_usage(self):
        try:
            values = []
            disk_partitions = psutil.disk_partitions(all=False)
            for partition in disk_partitions:
                usage = psutil.disk_usage(partition.mountpoint)
                device = {'device': partition.device,
                          'mountpoint': partition.mountpoint,
                          'fstype': partition.fstype,
                          'opts': partition.opts,
                          'total': usage.total,
                          'used': usage.used,
                          'free': usage.free,
                          'percent': usage.percent
                          }
                values.append(device)
            values = sorted(values, key=lambda device: device['device'])
            return values
        except Exception, e:
            self.logger.error('Error retrieving disks usage: %s' % e)
            return False

    def get_swapdisk_usage(self):
        try:
            mem = psutil.swap_memory()

            divisor = float(mem.total) * float(mem.used)
            if divisor > 0:
                percent = 100 / divisor
            else:
                percent = 0

            values = {'total': mem.total,
                      'used': mem.used,
                      'free': mem.free,
                      'sin': mem.sin,
                      'sout': mem.sout,
                      'percent': percent}
            return values
        except Exception, e:
            self.logger.error('Error retrieving swap disk usage: %s' % e)
            return False

    def get_disks_io(self):
        try:
            disks_io = []
            for k, v in psutil.disk_io_counters(perdisk=True).items():
                values = {'device': k,
                          'read_time': v._asdict()['read_time'],
                          'write_bytes': v._asdict()['write_bytes'],
                          'read_bytes': v._asdict()['read_bytes'],
                          'write_time': v._asdict()['write_time'],
                          'read_count': v._asdict()['read_count'],
                          'write_count': v._asdict()['write_count']
                          }
                disks_io.append(values)
            return disks_io
        except Exception, e:
            self.logger.error('Error retrieving disks IO rates: %s' % e)
            return False

    def get_network_io(self):
        try:
            values = dict(psutil.net_io_counters()._asdict())
            return values
        except Exception, e:
            self.logger.error('Error retrieving Network IO rates: %s' % e)
            return False
