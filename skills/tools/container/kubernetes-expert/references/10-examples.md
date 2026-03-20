# Examples

## 10.1 Deployment Examples

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: myapp
          image: myregistry.io/myapp:v1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
```

### Deployment with Sidecar

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:v1
          ports:
            - containerPort: 8080
        - name: log-shipper
          image: fluentd:v1
          volumeMounts:
            - name: logs
              mountPath: /var/log
      volumes:
        - name: logs
          emptyDir: {}
```

## 10.2 Service Examples

### ClusterIP Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      name: http
```

### NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
      name: http
```

### LoadBalancer Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
      name: http
```

### Headless Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  clusterIP: None
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 8080
```

## 10.3 Ingress Examples

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

### Ingress with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - myapp.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

## 10.4 ConfigMap & Secret Examples

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  DATABASE_URL: "postgres://db:5432/myapp"
  LOG_LEVEL: "info"
  CACHE_TTL: "300"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
stringData:
  username: admin
  password: changeme
```

### Using ConfigMap in Pod

```yaml
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: myapp-config
        key: LOG_LEVEL
volumeMounts:
  - name: config
    mountPath: /etc/config
volumes:
  - name: config
    configMap:
      name: myapp-config
```

## 10.5 NetworkPolicy Examples

### Deny All Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {}
  policyTypes:
    - Ingress
```

### Allow from Specific Namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-frontend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: production
        podSelector:
          matchLabels:
            app: frontend
```

### Allow Specific Ports

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-db
spec:
  podSelector:
    matchLabels:
      app: database
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: backend
      ports:
        - protocol: TCP
          port: 5432
```

## 10.6 RBAC Examples

### ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
```

### Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: myapp-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps", "pods", "services"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods/exec"]
    verbs: ["create"]
```

### RoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-rolebinding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRole for Cluster-wide Access

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: myapp-clusterrole
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list", "watch"]
```

## 10.7 kubectl Commands

### Pod Management

```bash
# Get pods
kubectl get pods -n production
kubectl get pods -o wide
kubectl get pods --show-labels

# Describe pod
kubectl describe pod <pod-name> -n production

# Logs
kubectl logs <pod-name> -n production
kubectl logs <pod-name> -f -n production
kubectl logs <pod-name> --previous -n production

# Execute in container
kubectl exec -it <pod-name> -n production -- /bin/sh
kubectl exec <pod-name> -n production -- env

# Port forward
kubectl port-forward <pod-name> 8080:80 -n production
```

### Deployment Management

```bash
# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -k ./manifests/

# Get deployments
kubectl get deployments -n production

# Scale
kubectl scale deployment myapp --replicas=5 -n production

# Rolling update
kubectl rollout status deployment/myapp -n production

# Rollback
kubectl rollout undo deployment/myapp -n production

# Restart
kubectl rollout restart deployment/myapp -n production
```

### Resource Management

```bash
# Get all resources
kubectl get all -n production

# Get resources with labels
kubectl get pods -l app=myapp -n production

# Delete resources
kubectl delete pod <pod-name> -n production
kubectl delete -f deployment.yaml

# Edit resources
kubectl edit deployment myapp -n production
kubectl patch deployment myapp -p '{"spec":{"replicas":3}}'
```

### Debugging

```bash
# Events
kubectl get events -n production --sort-by='.lastTimestamp'

# Top resources
kubectl top pod -n production
kubectl top node

# API resources
kubectl api-resources
kubectl explain pod

# Cluster info
kubectl cluster-info
kubectl get nodes
```