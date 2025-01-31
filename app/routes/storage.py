import os


from flask import render_template


from app import app, auth


@app.route('/df/')
@auth.login_required
def df():
    return render_template('df.html', title='Used space', current_page='df')


@app.route('/df/info/')
@auth.login_required
def df_info():
    return os.popen('df -h').read()    


@app.route('/lsblk/')
@auth.login_required
def lsblk():
    return render_template('lsblk.html', title='Devices', current_page='lsblk')


@app.route('/lsblk/info/')
@auth.login_required
def lsblk_info():
    return os.popen('lsblk').read()    
