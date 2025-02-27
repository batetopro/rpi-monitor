import json
import sys


from app import app
from app.reports import reports


@app.cli.command("chat")
def chat():
    while 1:
        query = sys.stdin.readline().strip()
        if query == 'quit':
            break

        if query in reports:
            data = reports[query]()
        else:
            data = False

        message = json.dumps(data)
        sys.stdout.write('{}\n'.format(len(message)))
        sys.stdout.write(message)
        sys.stdout.flush()


@app.cli.command("host")
def get_host():
    data = reports['host']()
    print(json.dumps(data))


@app.cli.command("net_interfaces")
def get_net_interfaces():
    data = reports['net_interfaces']()
    print(json.dumps(data))


@app.cli.command("platform")
def get_platform():
    data = reports['platform']()
    print(json.dumps(data))


@app.cli.command("usage")
def get_usage():
    data = reports['runtime']()
    print(json.dumps(data))
