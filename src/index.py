from kubernetes import client, config
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    return "Welcome to Kubernetes dashboard"

@app.get("/api/v1/listpods")
def main():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    pod_dict = {}
    for i in ret.items:
        pod_dict[i.status.pod_ip] = i.metadata.name
    return pod_dict