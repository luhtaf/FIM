import os, hashlib

## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address

def walk(dir):
    hasil=[]
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            hasil.append(os.path.join(root, name))
        # for name in dirs:
        #     print(os.path.join(root, name))
    return hasil

def list_file(dir):
    hasil=[]
    for filename in os.listdir(dir):
        filepath = os.path.join(dir, filename)
        if os.path.isfile(filepath):
            hasil.append(os.path.abspath(filepath))
    return hasil


def load_yaml(path):
    import yaml
    with open(path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def sha256(text):
    text_bytes = text.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(text_bytes)
    hash_value = sha256.hexdigest()
    return hash_value
