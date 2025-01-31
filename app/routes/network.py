import os


from flask import render_template


from app import app, auth


@app.route('/ipa/')
@auth.login_required
def ipa():
    return render_template('ipa.html', title='NICs', current_page='ipa')    


@app.route('/ipa/info/')
@auth.login_required
def ipa_info():
    return os.popen('ip a').read()
