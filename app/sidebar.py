from flask import url_for


from app import app


@app.context_processor
def register_sidebar():
    sidebar = [
        {
            'title': 'HOST',
            'children': [
                {
                    'name': 'host',
                    'title': 'Info',
                    'url': url_for('host'),
                    'icon': 'bi bi-motherboard',
                },
                {
                    'name': 'ps',
                    'title': 'Processes',
                    'url': url_for('process'),
                    'icon': 'bi bi-filetype-exe',
                },
                {
                    'name': 'systemctl',
                    'title': 'Services',
                    'url': url_for('systemctl'),
                    'icon': 'bi bi-wrench',
                },
            ],
        },
        {
            'title': 'CPU',
            'children': [
                {
                    'name': 'cpuinfo',
                    'title': 'Info',
                    'url': url_for('cpu'),
                    'icon': 'bi bi-cpu',
                },
            ],
        },
        {
            'title': 'STORAGE',
            'children': [
                {
                    'name': 'df',
                    'title': 'Used space',
                    'url': url_for('df'),
                    'icon': 'bi bi-device-hdd',
                },
                {
                    'name': 'lsblk',
                    'title': 'Devices',
                    'url': url_for('lsblk'),
                    'icon': 'bi bi-usb-drive',
                },
            ],
        },
        {
            'title': 'NETWORK',
            'children': [
                {
                    'name': 'ipa',
                    'title': 'NICs',
                    'url': url_for('ipa'),
                    'icon': 'bi bi-hdd-network',
                },
                {
                    'name': 'network_packets',
                    'title': 'Packets',
                    'url': url_for('network_packets'),
                    'icon': 'bi bi-box',
                },
            ],
        },
    ]

    return dict(sidebar=sidebar)