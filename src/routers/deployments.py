from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from kubernetes import client

from src.core import kubeconfig

templates = Jinja2Templates(directory='./src/templates')

router = APIRouter(
    prefix='/api/v1',
    tags=['deployment']
)

@router.get("/listdeploy", response_class=HTMLResponse)
async def list_all_pods(request: Request) -> list:
    kubeconfig.get_config()
    apps_v1 = client.AppsV1Api()
    resp = apps_v1.list_deployment_for_all_namespaces(watch=False)
    deployment_list = []
    for i in resp.items:
        deploy_data = {}
        deploy_data["name"] = i.metadata.name
        deploy_data["namespace"] = i.metadata.namespace
        deploy_data["replicas"] = i.spec.replicas
        deployment_list.append(deploy_data)
    return templates.TemplateResponse(request=request, name="deploylist.html", context={'context': deployment_list})

@router.get("/{namespace}/listdeploy", response_class=HTMLResponse)
async def list_all_pods(request: Request, namespace: str) -> list:
    kubeconfig.get_config()
    apps_v1 = client.AppsV1Api()
    resp = apps_v1.list_namespaced_deployment(namespace=namespace)
    deployment_list = []
    for i in resp.items:
        deploy_data = {}
        deploy_data["name"] = i.metadata.name
        deploy_data["namespace"] = i.metadata.namespace
        deploy_data["replicas"] = i.spec.replicas
        deployment_list.append(deploy_data)
    return templates.TemplateResponse(request=request, name="deploylist.html", context={'context': deployment_list})