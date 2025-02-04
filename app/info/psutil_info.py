import os
import socket


import psutil


class PsutilHostInfo:
    @property
    def cpu_frequency(self):
        if self._cpu_freq is None:
            self._cpu_freq = psutil.cpu_freq()
        return self._cpu_freq.current

    @property
    def cpu_idle(self):
        if self._cpu_times is None:
            self._cpu_times = psutil.cpu_times()
        return self._cpu_times.idle

    @property
    def cpu_max_frequency(self):
        if self._cpu_freq is None:
            self._cpu_freq = psutil.cpu_freq()
        return self._cpu_freq.max

    @property
    def cpu_system(self):
        if self._cpu_times is None:
            self._cpu_times = psutil.cpu_times()
        return self._cpu_times.system

    @property
    def cpu_temp(self):
        if self._cpu_temp is None:
            self._cpu_temp = self.read_cpu_temp()
        return self._cpu_temp

    @property
    def cpu_usage_percent(self):
        if self._cpu_usage_percent is None:
            self._cpu_usage_percent = psutil.cpu_percent(interval=1)
        return self._cpu_usage_percent

    @property
    def cpu_user(self):
        if self._cpu_times is None:
            self._cpu_times = psutil.cpu_times()
        return self._cpu_times.user

    @property
    def current_date(self):
        return self.read_current_date()

    @property
    def disk_io_read_bytes(self):
        if self._disk_io_counters is None:
            self._disk_io_counters = psutil.disk_io_counters()
        return self._disk_io_counters.read_bytes

    @property
    def disk_io_write_bytes(self):
        if self._disk_io_counters is None:
            self._disk_io_counters = psutil.disk_io_counters()
        return self._disk_io_counters.write_bytes

    @property
    def disk_space_available(self):
        if self._disk_space_available is None:
            self.read_disk_space()
        return self._disk_space_available
    
    @property
    def disk_space_total(self):
        return self.disk_space_available + self.disk_space_used

    @property
    def disk_space_used(self):
        if self._disk_space_used is None:
            self.read_disk_space()
        return self._disk_space_used

    @property
    def hostname(self):
        if self._hostname is None:
            self._hostname = self.read_hostname()
        return self._hostname

    @property
    def model(self):
        if self._model is None:
            self._model = self.read_model()
        return self._model

    @property
    def net_io_bytes_recv(self):
        if self._net_io_counters is None:
            self._net_io_counters = psutil.net_io_counters()
        return self._net_io_counters.bytes_recv

    @property
    def net_io_bytes_sent(self):
        if self._net_io_counters is None:
            self._net_io_counters = psutil.net_io_counters()
        return self._net_io_counters.bytes_sent

    @property
    def number_of_cpus(self):
        if self._number_of_cpus is None:
            self._number_of_cpus = psutil.cpu_count()
        return self._number_of_cpus

    @property
    def ram_free(self):
        return self.virtual_memory.free

    @property
    def ram_total(self):
        return self.virtual_memory.total

    @property
    def ram_used(self):
        return self.virtual_memory.used

    @property
    def ram_used_percent(self):
        return self.virtual_memory.percent

    @property
    def up_for(self):
        return self.read_up_for()

    @property
    def up_since(self):
        if self._up_since is None:
            self._up_since = self.read_up_since()
        return self._up_since

    @property
    def virtual_memory(self):
        if self._virtual_memory is None:
            self._virtual_memory = psutil.virtual_memory()
        return self._virtual_memory

    def __init__(self):
        self._cpu_freq = None
        self._cpu_temp = None
        self._cpu_times = None
        self._cpu_usage_percent = None
        self._hostname = None
        self._disk_io_counters = None
        self._disk_space_available = None
        self._disk_space_used = None
        self._model = None
        self._net_io_counters = None
        self._number_of_cpus = None
        self._up_since = None
        self._virtual_memory = None

    def read_cpu_temp(self):
        try:
            data = psutil.sensors_temperatures()
            return data['cpu_thermal'][0].current
        except Exception as ex:
            return None

    def read_current_date(self):
        return float(os.popen('date +%s').read().strip())

    def read_disk_space(self):
        usage = psutil.disk_usage('/')
        self._disk_space_available = usage.free
        self._disk_space_used = usage.used

    def read_hostname(self):
        return socket.gethostname()

    def read_model(self):
        try:
            with open('/proc/device-tree/model', 'r') as fp:
                return fp.read().rstrip('\0').strip()
        except Exception:
            return None

    def read_number_of_cpus(self):
        return int(os.popen('nproc').read().strip())

    def read_up_for(self):
        return self.current_date - self.up_since

    def read_up_since(self):
        return psutil.boot_time()
