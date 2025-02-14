import datetime
import os
import re
import socket
import subprocess


from app.settings import basedir


class HostInfo:
    @property
    def cpu_frequency(self):
        if self._cpu_frequency is None:
            self._cpu_frequency = self.read_cpu_frequency()
        return self._cpu_frequency

    @property
    def cpu_idle(self):
        if self._cpu_idle is None:
            self._cpu_idle = self.read_cpu_idle()
        return self._cpu_idle

    @property
    def cpu_max_frequency(self):
        if self._cpu_max_frequency is None:
            self._cpu_max_frequency = self.read_cpu_max_frequency()
        return self._cpu_max_frequency

    @property
    def cpu_temp(self):
        if self._cpu_temp is None:
            self._cpu_temp = self.read_cpu_temp()
        return self._cpu_temp

    @property
    def cpu_usage_percent(self):
        if self._cpu_usage_percent is None:
            self._cpu_usage_percent = self.read_cpu_usage_percent()
        return self._cpu_usage_percent

    @property
    def current_date(self):
        return self.read_current_date()

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
    def number_of_cpus(self):
        if self._number_of_cpus is None:
            self._number_of_cpus = self.read_number_of_cpus()
        return self._number_of_cpus

    @property
    def ram_free(self):
        if self._ram_free is None:
            self._ram_free = self.read_ram_free()
        return self._ram_free

    @property
    def ram_total(self):
        if self._ram_total is None:
            self._ram_total = self.read_ram_total()
        return self._ram_total

    @property
    def ram_used(self):
        return self.ram_total - self.ram_free

    @property
    def ram_used_percent(self):
        return round((self.ram_used / self.ram_total) * 100)

    @property
    def up_for(self):
        return self.read_up_for()

    @property
    def up_since(self):
        if self._up_since is None:
            self._up_since = self.read_up_since()
        return self._up_since

    def __init__(self):
        self._cpu_frequency = None
        self._cpu_idle = None
        self._cpu_temp = None
        self._cpu_max_frequency = None
        self._cpu_usage_percent = None

        self._disk_space_available = None
        self._disk_space_used = None

        self._hostname = None

        self._model = None
        self._number_of_cpus = None
    
        self._ram_free = None
        self._ram_total = None

        self._up_since = None

    def read_cpu_frequency(self):
        return round(
            float(
                os.popen(
                    "/bin/cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
                ).read()
            )
            / 1000000,
            2,
        )    
    
    def read_cpu_idle(self):
        return 100 - round(
            float(
                os.popen(
                    "/bin/grep 'cpu ' /proc/stat | /usr/bin/awk '{usage=(($2+$4)*100)/($2+$4+$5)} END {print usage}'"
                ).read()
            )
        )

    def read_cpu_max_frequency(self):
        return round(
            float(
                os.popen(
                    "/bin/cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
                ).read()
            )
            / 1000000,
            2,
        )

    def read_cpu_temp(self):
        return round(
            float(os.popen("/bin/cat /sys/class/thermal/thermal_zone0/temp").read()) / 1000
        )

    def read_cpu_usage_percent(self):
        process = subprocess.Popen(
            "/bin/bash " + os.path.join(basedir, "current_cpu.sh"),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        return round(float(stdout.decode()))

    def read_current_date(self):
        return os.popen('date +%s').read().strip()

    def read_disk_space(self):
        data = os.popen('df').read()
        
        available = 0
        used = 0
        regex = re.compile(r'\s+')

        for k, line in enumerate(data.splitlines()):
            if k == 0:
                continue
            line = line.strip()
            parts = regex.split(line)
            
            used += int(parts[2])
            available += int(parts[3])

        self._disk_space_available = available
        self._disk_space_used = used

    def read_hostname(self):
        return socket.gethostname()

    def read_model(self):
        return os.popen("/bin/cat /sys/firmware/devicetree/base/model").read().rstrip('\0').strip()

    def read_number_of_cpus(self):
        return int(os.popen('nproc').read().strip())

    def read_ram_free(self):
        return round(
            int(
                os.popen(
                    "/bin/grep 'MemAvailable: ' /proc/meminfo | /usr/bin/awk '{free=$2} END {print free}'"
                ).read()
            )
            / 1000
        )

    def read_ram_total(self):
        return round(
            int(
                os.popen(
                    "/bin/grep 'MemTotal: ' /proc/meminfo | /usr/bin/awk '{total=$2} END {print total}'"
                ).read()
            )
            / 1000
        )
    
    def read_up_for(self):
        return os.popen("/usr/bin/uptime -p").read().strip()
    
    def read_up_since(self):
        return datetime.datetime.strptime(
            os.popen("/usr/bin/uptime -s").read().strip(),
            '%Y-%m-%d %H:%M:%S'
        ).timestamp()
