import os


from flask import json, render_template


from app import app, auth
from app.info.network_packets import NetworkPacketsInfo


@app.route('/ipa/')
@auth.login_required
def ipa():
    return render_template('ipa.html', title='NICs', current_page='ipa')    


@app.route('/ipa/info/')
@auth.login_required
def ipa_info():
    return os.popen('ip a').read()


@app.route('/network-packets/')
@auth.login_required
def network_packets():
    return render_template(
        'network_packets.html',
        title='Network packets',
        current_page='network_packets'
    )


@app.route('/network-packets/info/')
@auth.login_required
def network_packets_info():
    info = NetworkPacketsInfo()
    return json.dumps(info.data)
