from flask import render_template


from app import app, auth


@app.route('/network/ifconfig/')
@auth.login_required
def ifconfig():
    return render_template('ifconfig.html', title='ifconfig', current_page='ifconfig')    


@app.route('/network/ipa/')
@auth.login_required
def ipa():
    return render_template('ipa.html', title='ip -a', current_page='ipa')    
