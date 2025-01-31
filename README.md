




## Installation
```
# Install pip before continuing
sudo apt-get install python3-pip

# Install virtualenv
sudo apt-get install python3-virtualenv


# Create a virtual environment
python3 -m virtualenv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
# Change 0.0.0.0:5000 to whereever you want RPi monitor to listen at
gunicorn wsgi:app -b 0.0.0.0:5000
```





