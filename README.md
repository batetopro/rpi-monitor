
## Installation
```
# Install pip before continuing
sudo apt-get install python3-pip

# Install virtualenv
sudo apt-get install python3-virtualenv

# Create a user for the monitoring
sudo adduser --gecos 'Raspberry monitoring' rpi-monitor

# Lock the user
sudo usermod -L rpi-monitor

# Login as the rpi-monitor user and go to its home
sudo su rpi-monitor
cd ~

# Checkout the repo and enter it
git clone https://github.com/batetopro/rpi-monitor.git
cd rpi-monitor

# Create a virtual environment
python3 -m virtualenv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Logout the rpi-monitor user
exit
```
Configure the systemctl service.
```
sudo nano /etc/systemd/system/rpi-monitor.service
```
Enter the following:
```
[Unit]
Description=RPi monitor (Monitor your raspberries)
After=syslog.target
After=network.target

[Service]
RestartSec=2s
Type=simple
User=rpi-monitor
Group=rpi-monitor
WorkingDirectory=/home/rpi-monitor/rpi-monitor
ExecStart=/home/rpi-monitor/rpi-monitor/venv/bin/gunicorn wsgi:app -b 127.0.0.1:5000
Restart=always
Environment=USER=rpi-monitor
HOME=/home/rpi-monitor

[Install]
WantedBy=multi-user.target
```

Activate the new service
```
sudo systemctl enable rpi-monitor.service
sudo systemctl start rpi-monitor.service
```

Install Nginx
```
sudo apt-get install nginx
```

Create Nginx configration file `/etc/nginx/conf.d/rpi-monitor.conf`

'''
server {
   listen 80;

   server_name rpi-monitor.localhost;    # Change localhost to the real name of the server

   location / {
     proxy_set_header        X-Real-IP $remote_addr;
     proxy_set_header        X-Forwarded-For $remote_addr;
     proxy_set_header        X-Forwarded-Proto $scheme;
     proxy_set_header        Host $host;
     proxy_intercept_errors  on;
     proxy_pass http://127.0.0.1:5000/;  # Change 5000 to the port set in systemctl config
   }
}
'''

Restart Nginx
```
sudo systemctl restart nginx
```
