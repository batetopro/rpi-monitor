from flask import render_template


from app import app, auth


@app.route('/cpu/')
@auth.login_required
def cpu():
    return render_template('cpuinfo.html', title='CPU info', current_page='cpuinfo')



@app.route('/cpu/info/')
@auth.login_required
def cpuinfo():
    with open('/proc/cpuinfo', 'r') as fp:
        data = fp.read().strip()
    
    return data
