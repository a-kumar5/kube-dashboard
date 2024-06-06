# kube-scheduler
Project to connect to eks cluster and perform some patching tasks.

If the container is not able to fetch the pod list, create below ClusterRole and ClusterRoleBinding

```yaml
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: pods-list
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: pods-list
  apiGroup: rbac.authorization.k8s.io
```

# when pod is running in minikube and you want expose the application use port-forwarding

` kubectl port-forward kube-timed-scheduler-deployment-6bf7974f5c-7wst5 8000:8000`
