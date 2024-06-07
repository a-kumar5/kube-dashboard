from kubernetes import config

def get_config():
    try:
        config.load_incluster_config()
        print("Loaded incluster config")
    except:
        config.load_kube_config(config_file='/home/akumar/.kube/config')
        print("Loaded kubeconfig from local")