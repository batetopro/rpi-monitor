import os


from flask import json, render_template


from app import app, auth




@app.route('/systemctl')
@auth.login_required
def systemctl():
    return render_template('systemctl.html', title='Services', current_page='systemctl')


@app.route('/systemctl/info/')
@auth.login_required
def systemctl_info():
    data = []
    
    for line in os.popen('service --status-all').read().splitlines():
        if line.startswith(' [ + ]  '):
            data.append((True, line[len(' [ + ]  '):]))
        elif line.startswith(' [ - ]  '):
            data.append((False, line[len(' [ - ]  '):]))

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
