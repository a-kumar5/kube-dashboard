import redis

from fastapi import FastAPI
from requests_cache import CachedSession

from src.core import kubeauth
from kubernetes import config, client

app = FastAPI()

session = CachedSession(
    cache_name='cache/kube_config',
    expire_after=600
)
@app.get("/")
async def main():
    return "Welcome to Kubernetes dashboard"

@app.get("/api/v1/kubeconfig")
async def get_kubeconfig():
    kube_config = kubeauth.get_config()
    return kube_config

@app.get("/api/v1/listpods")
async def list_pod(kube_config: dict):
    if kube_config:
        print("cache hit")
        config.load_kube_config_from_dict(config_dict=kube_config)
    else:
    config.load_kube_config_from_dict(config_dict=kube_config)
    v1_api = client.CoreV1Api()  # api_client
    pods = v1_api.list_namespaced_pod("psc-dev")
    podlist = []
    for pod in pods.items:
        podlist.append(pod.metadata.name)
    return podlist
