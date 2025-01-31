from app import app
from app.info.host import HostInfo


@app.cli.command("stats")
def get_stats():
    host_info = HostInfo()

    print('Hello from: ' + host_info.hostname)
    print('Model: ' + host_info.model)
    
    print('CPU usage: {}'.format(host_info.cpu_usage_percent))
    print('CPU frequency: {}'.format(host_info.cpu_frequency))
    print('CPU max frequency: {}'.format(host_info.cpu_max_frequency))
    print('CPU Temperature: {}'.format(host_info.cpu_temp))
    
    print('RAM total: {}'.format(host_info.ram_total))
    print('RAM free: {}'.format(host_info.ram_free))
    print('RAM used: {}'.format(host_info.ram_used))
    print('RAM used percent: {}'.format(host_info.ram_used_percent))
    
    print('Up for: {}'.format(host_info.up_for))
    print('Up since: {}'.format(host_info.up_since))
    print('Current date: {}'.format(host_info.current_date))

    print(host_info.read_platform())
    