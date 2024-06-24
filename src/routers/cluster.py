from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from kubernetes import client
from src.core import kubeconfig

router = APIRouter(
    prefix='/api/v1',
    tags=['cluster']
)

@router.get("/listnodes", status_code=status.HTTP_200_OK)
async def list_all_nodes():
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    nodes_resp = v1.list_node()
    node_list = []
    for node in nodes_resp.items:
        node_data = {}
        node_data[node.metadata.ip] = node.metadata.name
        node_list.append(node_data)
    return JSONResponse(content=node_list[0])

@router.get("/listns", status_code=status.HTTP_200_OK)
async def list_namespaces():
    kubeconfig.get_config()
    v1 = client.CoreV1Api()
    namespaces_resp = v1.list_namespace()
    namespace = {}
    SN = 1
    for ns in namespaces_resp.items:
        namespace[SN] = ns.metadata.name
        SN += 1
    return JSONResponse(content=namespace)

