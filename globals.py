# =============================================================================
# Imports
#  =============================================================================
import os
import subprocess

# Kivy imports
import kivy
kivy.require ('1.10.0')

#Widgets
from kivy.uix.label import Label


# =============================================================================
# Globals
# =============================================================================
STATUS_BAR = Label(text="Problem detected.", size_hint=(1, .1))
WEBROOT = "http://localhost:8082/"
LOCAL_CONFIG_PATH = ".shaLocalConfig"

try:
    HOSTNAME = os.environ['COMPUTERNAME']
except KeyError:
    import socket
    HOSTNAME = socket.gethostname()

try:
    output = subprocess.run('ipconfig', check=True, stdout=subprocess.PIPE)
    IP_ADDR = "unknown"
    for line in output.stdout.split(b"\n"):
        if b"ipv4" in line:
            IP_ADDR = str(line).split(":")[1].strip().replace("\\r'", "")
except FileNotFoundError:
    IP_ADDR = "unknown"

# =============================================================================
# Functions
# =============================================================================

# =============================================================================
# Classes
# =============================================================================
