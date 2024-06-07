from kubernetes import client
from fastapi import APIRouter
from src.core import kubeconfig


router = APIRouter(
    prefix='/pods',
    tags=['pods']
)

@router.get("/api/v1/listpods")
async def list_all_pods():
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    pod_dict = {}
    for i in ret.items:
        pod_dict[i.status.pod_ip] = i.metadata.name
    return pod_dict

@router.get("/api/v1/{namespace}/listpods")
async def list_pods_in_namespace(namespace: str) -> dict:
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_namespaced_pod(namespace=namespace)
    pod_dict = {}
    for i in ret.items:
        pod_dict[i.status.pod_ip] = i.metadata.name
    return pod_dict