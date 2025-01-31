from flask import json


from app import app, auth


from flask import render_template


@app.route('/systemctl')
@auth.login_required
def systemctl():
    return render_template('systemctl.html', title='Systemctl status', current_page='systemctl')
