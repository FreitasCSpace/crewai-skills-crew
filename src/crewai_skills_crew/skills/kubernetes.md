# Skill: kubernetes

## Purpose
Manage Kubernetes clusters, deployments, services, and pods using `kubectl`.

## When to use
- Deploying or updating applications on Kubernetes
- Inspecting pod status, logs, or events
- Managing services, ingresses, configmaps, and secrets
- Scaling deployments or debugging issues
- Applying manifests or Helm charts

## Prerequisites
- `kubectl` installed: `curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/$(uname -s | tr A-Z a-z)/amd64/kubectl" && chmod +x kubectl && mv kubectl /usr/local/bin/`
- Kubeconfig set: `export KUBECONFIG=~/.kube/config`
- Verify: `kubectl cluster-info && kubectl get nodes`

## How to execute

**Cluster info:**
```bash
kubectl cluster-info
kubectl get nodes -o wide
kubectl get namespaces
```

**List resources:**
```bash
kubectl get pods -n NAMESPACE
kubectl get deployments -n NAMESPACE
kubectl get services -n NAMESPACE
kubectl get ingress -n NAMESPACE
kubectl get all -n NAMESPACE
```

**Pod operations:**
```bash
# Describe a pod (events, conditions, containers)
kubectl describe pod POD_NAME -n NAMESPACE

# View logs
kubectl logs POD_NAME -n NAMESPACE --tail=100
kubectl logs POD_NAME -n NAMESPACE -c CONTAINER_NAME  # specific container
kubectl logs -l app=myapp -n NAMESPACE --tail=50       # by label

# Exec into a pod
kubectl exec -it POD_NAME -n NAMESPACE -- /bin/sh

# Port forward
kubectl port-forward pod/POD_NAME 8080:80 -n NAMESPACE
```

**Deploy from a manifest:**
```bash
cat > deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myregistry/myapp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: default
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
EOF

kubectl apply -f deployment.yaml
```

**Scale a deployment:**
```bash
kubectl scale deployment myapp --replicas=5 -n NAMESPACE
```

**Rolling update:**
```bash
kubectl set image deployment/myapp myapp=myregistry/myapp:v2.0 -n NAMESPACE
kubectl rollout status deployment/myapp -n NAMESPACE
kubectl rollout undo deployment/myapp -n NAMESPACE   # rollback
```

**Secrets and ConfigMaps:**
```bash
# Create a secret
kubectl create secret generic myapp-secrets \
  --from-literal=database-url='postgres://...' \
  --from-literal=api-key='secret123' -n NAMESPACE

# Create a configmap
kubectl create configmap myapp-config \
  --from-file=config.yaml -n NAMESPACE

# View secrets (base64 encoded)
kubectl get secret myapp-secrets -n NAMESPACE -o jsonpath='{.data}' | python3 -m json.tool
```

**Helm:**
```bash
# Add a chart repo
helm repo add bitnami https://charts.bitnami.com/bitnami && helm repo update

# Install a chart
helm install my-release bitnami/postgresql -n NAMESPACE --set auth.postgresPassword=pass

# List releases
helm list -n NAMESPACE

# Upgrade
helm upgrade my-release bitnami/postgresql -n NAMESPACE -f values.yaml
```

**Debug:**
```bash
# Events in namespace
kubectl get events -n NAMESPACE --sort-by=.lastTimestamp | tail -20

# Resource usage
kubectl top pods -n NAMESPACE
kubectl top nodes
```

## Output contract
- stdout: resource info, logs, or status
- exit_code 0: success
- exit_code 1+: connection error, resource not found, or permission denied

## Evaluate output
If "connection refused": check kubeconfig and cluster availability.
If pod is CrashLoopBackOff: check logs with `kubectl logs --previous`.
If ImagePullBackOff: verify image name and registry credentials.
