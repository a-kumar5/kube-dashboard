from kubernetes import client, config

def get_config():
     return config.load_incluster_config()