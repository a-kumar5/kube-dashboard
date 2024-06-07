from kubernetes import client
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.core import kubeconfig

templates = Jinja2Templates(directory='./src/templates')

router = APIRouter(
    prefix='/api/v1',
    tags=['pods']
)

@router.get("/listpods", response_class=HTMLResponse)
async def list_all_pods(request: Request):
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    pod_dict = {}
    for i in ret.items:
        pod_dict[str(i.status.pod_ip)] = i.metadata.name
    print(pod_dict)
    return templates.TemplateResponse(request=request, name="podlist.html", context={'context': pod_dict})

@router.get("/{namespace}/listpods")
async def list_pods_in_namespace(request: Request, namespace: str) -> dict:
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    ret = v1.list_namespaced_pod(namespace=namespace)
    pod_dict = {}
    for i in ret.items:
        pod_dict[i.status.pod_ip] = i.metadata.name
    return templates.TemplateResponse(request=request, name="podlist.html", context={'context': pod_dict})