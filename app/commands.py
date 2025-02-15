import json


from app import app
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
    host_info = PsutilHostInfo()

    data = {
        'cpu_usage': host_info.cpu_usage_percent,
        'cpu_frequency': host_info.cpu_frequency,
        'cpu_temperature': host_info.cpu_temp,
        'current_date': host_info.current_date,
        'disk_io_read_bytes': host_info.disk_io_read_bytes,
        'disk_io_write_bytes': host_info.disk_io_write_bytes,
        'disk_space_available': host_info.disk_space_available,
        'disk_space_used': host_info.disk_space_used,
        'disk_space_total': host_info.disk_space_total,
        'disk_partitions': host_info.disk_partitions,
        'net_interfaces': host_info.net_interfaces,
        'net_io_bytes_recv': host_info.net_io_bytes_recv,
        'net_io_bytes_sent': host_info.net_io_bytes_sent,
        'ram': host_info.ram_used,
        'swap_used': host_info.swap_used,
        'swap_total': host_info.swap_total,
    }

    print(json.dumps(data))
