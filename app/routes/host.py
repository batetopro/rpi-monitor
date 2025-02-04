from flask import json, render_template


from app import app, auth
from app.info.platform_info import PlatformInfo
from app.info.psutil_info import PsutilHostInfo


@app.route('/')
@auth.login_required
def host():
    return render_template('host.html', title='Host', current_page='host')


@app.route('/host/info/')
@auth.login_required
def host_info():
    info = PsutilHostInfo()
    platform = PlatformInfo.read()

    data = {
        'hostname': info.hostname,
        'model': info.model,
        'current_date': info.current_date,
        'cpu': {
            'usage': info.cpu_usage_percent,
            'frequency': info.cpu_frequency,
            'max_frequency': info.cpu_max_frequency,
            'temperature': info.cpu_temp,
            'number': info.number_of_cpus,
        },
        'disk_io': {
            'read_bytes': info.disk_io_read_bytes,
            'write_bytes': info.disk_io_write_bytes,
        },
        'disk_space': {
            'available': info.disk_space_available,
            'used': info.disk_space_used,
            'total':  info.disk_space_total,
        },
        'network': {
            'received': info.net_io_bytes_recv,
            'transmitted': info.net_io_bytes_sent,
        },
        'ram': {
            'total': info.ram_total,
            'free': info.ram_free,
            'used': info.ram_used,
            'used_percent': info.ram_used_percent,
        },
        'swap': {
            'total': info.swap_total,
            'free': info.swap_free,
            'used': info.swap_used,
            'used_percent': info.swap_used_percent,
        },
        'uptime': {
            'for': info.up_for,
            'since': info.up_since,
        },
        'platform': {
            'system': platform['system'],
            'processor': platform['processor'],
            'machine': platform['machine'],
            'pretty_name': platform['pretty_name'],
        },
    }
   
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
