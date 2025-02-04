import datetime
import json


from app import app
from app.info.host import HostInfo
from app.info.platform_info import PlatformInfo
from app.info.psutil_info import PsutilHostInfo


@app.cli.command("host")
def get_host():
    host_info = PsutilHostInfo()
    platform_info = PlatformInfo.read()

    data = {
        'hostname': host_info.hostname,
        'model': host_info.model,
        'os_name': platform_info['pretty_name'],
        'system': platform_info['system'],
        'machine': platform_info['machine'],
        'processor': platform_info['processor'],
        'platform': platform_info['platform'],
        'up_since': host_info.up_since,
        'max_cpu_frequency': host_info.cpu_max_frequency,
        'total_ram': host_info.ram_total,
        'number_of_cpus': host_info.number_of_cpus,
    }

    print(json.dumps(data))


@app.cli.command("usage")
def get_usage():
    host_info = HostInfo()

    data = {
        'cpu_usage': host_info.cpu_usage_percent,
        'cpu_frequency': host_info.cpu_frequency,
        'cpu_temperature': host_info.cpu_temp,
        'ram': host_info.ram_used,
        'disk_space_available': host_info.disk_space_available,
        'disk_space_used': host_info.disk_space_used,
        'current_date': host_info.current_date,
    }

    print(json.dumps(data))
