from subprocess import Popen, PIPE


from flask import render_template


from app import app, auth





@app.route('/process/')
@auth.login_required
def process():
    return render_template('process.html', title='Process info', current_page='ps')



@app.route('/process/info/')
@auth.login_required
def process_info():
    process = Popen(['ps', '-aux'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout
