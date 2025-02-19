import os


from app.info.platform_info import PlatformInfo
from app.info.psutil_info import PsutilHostInfo


def cpu_percent():
    host_info = PsutilHostInfo()
    return {
        'cpu_usage': host_info.cpu_usage_per_cpu
    }


def host():
    host_info = PsutilHostInfo()

    data = {
        'hostname': host_info.hostname,
        'up_since': host_info.up_since,
        'min_cpu_frequency': host_info.cpu_min_frequency,
        'max_cpu_frequency': host_info.cpu_max_frequency,
        'total_ram': host_info.ram_total,
        'number_of_cpus': host_info.number_of_cpus,
    }

    return data


def net_interfaces():
    host_info = PsutilHostInfo()
    return {
        'net_interfaces': host_info.net_interfaces,
    }


def platform():
    host_info = PsutilHostInfo()
    platform_info = PlatformInfo.read()

    data = {
        'model': host_info.model,
        'os_name': platform_info['pretty_name'],
        'system': platform_info['system'],
        'machine': platform_info['machine'],
        'processor': platform_info['processor'],
        'platform': platform_info['platform'],
    }

    return data


def runtime():
    host_info = PsutilHostInfo()
    current_date = host_info.current_date

    for partition in host_info.disk_partitions:
        dev = os.path.basename(partition['device'])
        if dev in host_info.disk_io_counters:
            counters = host_info.disk_io_counters[dev]
            partition['io_read_bytes'] = counters.read_bytes
            partition['io_read_count'] = counters.read_count
            partition['io_read_time'] = counters.read_time
            partition['io_write_count'] = counters.write_count
            partition['io_write_bytes'] = counters.write_bytes
            partition['io_write_time'] = counters.write_time

    return {
        'cpu_usage': host_info.cpu_usage_percent,
        'cpu_frequency': host_info.cpu_frequency,
        'cpu_temperature': host_info.cpu_temp,
        'current_date': current_date,
        'disk_io_read_bytes': host_info.disk_io_read_bytes,
        'disk_io_write_bytes': host_info.disk_io_write_bytes,
        'disk_space_available': host_info.disk_space_available,
        'disk_space_used': host_info.disk_space_used,
        'disk_space_total': host_info.disk_space_total,
        'disk_partitions': host_info.disk_partitions,
        'net_io_bytes_recv': host_info.net_io_bytes_recv,
        'net_io_bytes_sent': host_info.net_io_bytes_sent,
        'net_io_counters': host_info.net_io_counters,
        'ram': host_info.ram_used,
        'swap_used': host_info.swap_used,
        'swap_total': host_info.swap_total,
    }


reports = {
    'cpu_percent': cpu_percent,
    'host': host,
    'net_interfaces': net_interfaces,
    'platform': platform,
    'runtime': runtime,
}
