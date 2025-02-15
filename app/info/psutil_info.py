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
    def disk_io_counters(self):
        if self._disk_io_counters is None:
            self._disk_io_counters = psutil.disk_io_counters(perdisk=True)
        return self._disk_io_counters

    @property
    def disk_io_read_bytes(self):
        result = 0
        for _, counters in self.disk_io_counters.items():
            result += counters.read_bytes
        return result

    @property
    def disk_io_write_bytes(self):
        result = 0
        for _, counters in self.disk_io_counters.items():
            result += counters.write_bytes
        return result

    @property
    def disk_partitions(self):
        if self._disk_partitions is None:
            self.read_disk_space()
        return self._disk_partitions

    @property
    def disk_space_available(self):
        if self._disk_space_available is None:
            self.read_disk_space()
        return self._disk_space_available

    @property
    def disk_space_total(self):
        if self._disk_space_total is None:
            self.read_disk_space()
        return self._disk_space_total

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
    def net_interfaces(self):
        interfaces = []

        for name, addresses in psutil.net_if_addrs().items():
            info = {
                'name': name,
                'ip4_address': None,
                'ip6_address': None,
                'addresses': []
            }

            for address in addresses:
                info['addresses'].append({
                    'family': address.family.name,
                    'address': address.address,
                    'netmask': address.netmask,
                    'broadcast': address.broadcast,
                    'ptp': address.ptp,
                })

                if address.family.name == 'AF_INET':
                    info['ip4_address'] = address.address

                if address.family.name == 'AF_INET6':
                    info['ip6_address'] = address.address

            interfaces.append(info)

        return interfaces

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
    def swap_free(self):
        return self.swap_memory.free

    @property
    def swap_memory(self):
        if self._swap_memory is None:
            self._swap_memory = psutil.swap_memory()
        return self._swap_memory

    @property
    def swap_total(self):
        return self.swap_memory.total

    @property
    def swap_used(self):
        return self.swap_memory.used

    @property
    def swap_used_percent(self):
        return self.swap_memory.percent

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
        self._disk_partitions = None
        self._disk_space_available = None
        self._disk_space_total = None
        self._disk_space_used = None
        self._model = None
        self._net_io_counters = None
        self._number_of_cpus = None
        self._swap_memory = None
        self._up_since = None
        self._virtual_memory = None

    def read_cpu_temp(self):
        try:
            data = psutil.sensors_temperatures()
            return data['cpu_thermal'][0].current
        except Exception:
            return None

    def read_current_date(self):
        return float(os.popen('date +%s').read().strip())

    def read_disk_space(self):
        self._disk_partitions = []
        self._disk_space_available = 0
        self._disk_space_total = 0
        self._disk_space_used = 0

        for partition in psutil.disk_partitions():
            usage = psutil.disk_usage(partition.mountpoint)
            self._disk_partitions.append({
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'opts': partition.opts,
                'space_available': usage.free,
                'space_total': usage.total,
                'space_used': usage.used,
                'io_read_bytes': None,
                'io_read_count': None,
                'io_read_time': None,
                'io_write_count': None,
                'io_write_bytes': None,
                'io_write_time': None,
            })
            self._disk_space_available += usage.free
            self._disk_space_total += usage.total
            self._disk_space_used += usage.used

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
