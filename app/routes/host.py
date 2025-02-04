from flask import json, render_template


from app import app, auth
from app.info.host import HostInfo
from app.info.network_packets import NetworkPacketsInfo


@app.route('/')
@auth.login_required
def host():
    return render_template('host.html', title='Host', current_page='host')


@app.route('/host/info/')
@auth.login_required
def host_info():
    info = HostInfo()
    platform = info.read_platform()
    network_packets_info = NetworkPacketsInfo()

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
        'ram': {
            'total': info.ram_total,
            'free': info.ram_free,
            'used': info.ram_used,
            'used_percent': info.ram_used_percent,
        },
        'uptime': {
            'for': info.up_for,
            'since': info.up_since,
            'idle': info.cpu_idle,
        },
        'platform': {
            'system': platform['system'],
            'processor': platform['processor'],
            'machine': platform['machine'],
            'pretty_name': platform['pretty_name'],
        },
        'disk_space': {
            'available': info.disk_space_available,
            'used': info.disk_space_used,
            'total':  info.disk_space_total,
        },
        'network': {
            'received': network_packets_info.total_recevied_bytes,
            'transmitted': network_packets_info.total_transmitted_bytes,
        }
    }
   
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
