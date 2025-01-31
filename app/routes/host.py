from flask import json


from app import app, auth
from app.info.host import HostInfo


from flask import render_template


@app.route('/')
@auth.login_required
def host():
    return render_template('host.html', title='Host', current_page='host')


@app.route('/host/info/')
@auth.login_required
def host_info():
    info = HostInfo()
    platform = info.read_platform()

    data = {
        'hostname': info.hostname,
        'model': info.model,
        'current_date': info.current_date,
        'cpu': {
            'usage': info.cpu_usage_percent,
            'frequency': info.cpu_frequency,
            'max_frequency': info.cpu_max_frequency,
            'temperature': info.cpu_temp,
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
        }
    }
   
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
