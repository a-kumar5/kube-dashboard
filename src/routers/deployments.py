from datetime import datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from kubernetes import client

from src.core import kubeconfig

templates = Jinja2Templates(directory='./src/templates')

router = APIRouter(
    prefix='/api/v1',
    tags=['deployment']
)

@router.get("/listdeploy", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def list_all_deployments(request: Request) -> list:
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

@router.get("/namespace/{namespace}/listdeploy", response_class=HTMLResponse)
async def list_all_namespace_deployments(request: Request, namespace: str) -> list:
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

@router.post("/namespace/{namespace}/deployments/{name}/replica/{count}", status_code=status.HTTP_200_OK)
async def update_replicas(namespace: str, name: str, count: int):
    kubeconfig.get_config()
    apps_v1 = client.AppsV1Api()
    body = {"spec":{"replicas": count}}
    resp = apps_v1.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
    return JSONResponse(content={"message": "Update the replicas"})

@router.get("/namespace/{namespace}/deployments/{name}/restart", status_code=status.HTTP_200_OK)
async def restart_deployment(namespace: str, name: str):
    kubeconfig.get_config()
    apps_v1 = client.AppsV1Api()
    body = {
            "spec": {
                "template": {
                    "metadata": {
                         "annotations": {
                            "kubedashboard.kubernetes.io/restartedAt": datetime.now()
                            }
                        }
                    }
                }
            }
    resp = apps_v1.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
    return JSONResponse(content={"message": "Rollout restart started"})