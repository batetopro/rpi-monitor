from flask import json


from app import app, auth


from flask import render_template


@app.route('/cpu/info/')
@auth.login_required
def cpuinfo():
    return render_template('cpuinfo.html', title='CPU info', current_page='cpuinfo')
