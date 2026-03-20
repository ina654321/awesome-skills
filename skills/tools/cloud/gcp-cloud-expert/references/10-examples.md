# Examples

## 10.1 Project Setup

```bash
# Create project
gcloud projects create my-project --name="My Project"

# Set active project
gcloud config set project my-project

# Enable APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com

# Create service account
gcloud iam service-accounts create my-sa \
  --display-name="My Service Account"

# Grant roles
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:my-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/compute.admin"
```

## 10.2 GKE Cluster

```bash
# Create cluster
gcloud container clusters create my-cluster \
  --zone=us-central1-a \
  --node-pool-name=default-pool \
  --num-nodes=3 \
  --machine-type=e2-medium

# Get credentials
gcloud container clusters get-credentials my-cluster \
  --zone=us-central1-a

# Create node pool
gcloud container node-pools create my-pool \
  --cluster=my-cluster \
  --zone=us-central1-a \
  --num-nodes=2 \
  --machine-type=n2-standard-4
```

## 10.3 Cloud Run Deployment

```bash
# Build and deploy
gcloud run deploy my-service \
  --image gcr.io/my-project/my-image \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Update service
gcloud run deploy my-service \
  --image gcr.io/my-project/my-image:v2 \
  --platform managed \
  --region us-central1

# List services
gcloud run services list --platform managed --region us-central1
```

## 10.4 BigQuery Operations

```bash
# Create dataset
bq mk my_dataset

# Create table
bq mk -t my_dataset.my_table \
  name:STRING,age:INT64,timestamp:TIMESTAMP

# Run query
bq query --use_legacy_sql=false \
  "SELECT * FROM my_dataset.my_table WHERE age > 21"

# Load data
bq load my_dataset.my_table \
  gs://my-bucket/data.csv \
  name:STRING,age:INT64
```

## 10.5 Cloud Storage

```bash
# Create bucket
gsutil mb -l us-central1 gs://my-bucket

# Copy files
gsutil cp file.txt gs://my-bucket/

# Set lifecycle policy
gsutil lifecycle set lifecycle.json gs://my-bucket

# Make public
gsutil iam ch allUsers:objectViewer gs://my-bucket
```

## 10.6 Deployment Manager Template

```yaml
# config.yaml
resources:
- name: my-vm
  type: compute.v1.instance
  properties:
    zone: us-central1-a
    machineType: zones/us-central1-a/machineTypes/e2-medium
    disks:
    - deviceName: boot
      type: PERSISTENT
      boot: true
      initializeParams:
        sourceImage: projects/debian-cloud/global/images/debian-11
    networkInterfaces:
    - network: global/networks/default
      accessConfigs:
      - type: ONE_TO_ONE_NAT
```

```bash
# Deploy
gcloud deployment-manager deployments create my-deployment \
  --config config.yaml
```

## 10.7 Cloud Functions

```python
# main.py
def hello_http(request):
    from flask import Flask, request as req
    app = Flask(__name__)
    
    with app.app_context():
        name = req.args.get('name', 'World')
        return f'Hello {name}!'
```

```bash
# Deploy
gcloud functions deploy my-function \
  --runtime python311 \
  --trigger-http \
  --region us-central1
```

## 10.8 VPC Setup

```bash
# Create custom VPC
gcloud compute networks create my-vpc \
  --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create my-subnet \
  --network my-vpc \
  --region us-central1 \
  --range 10.0.0.0/24

# Create firewall rules
gcloud compute firewall-rules create allow-internal \
  --network my-vpc \
  --allow tcp,udp,icmp \
  --source-ranges 10.0.0.0/24
```

## 10.9 IAM Policy

```bash
# Grant single role
gcloud projects add-iam-policy-binding my-project \
  --member=user:user@example.com \
  --role=roles/viewer

# Grant multiple roles
gcloud projects add-iam-policy-binding my-project \
  --member=serviceAccount:sa@project.iam.gserviceaccount.com \
  --role=roles/storage.objectAdmin \
  --role=roles/bigquery.dataEditor
```

## 10.10 Budget Alert

```bash
# Create budget
gcloud billing budgets create \
  --billing-account=XXXXX \
  --display-name="Monthly Budget" \
  --budget-amount=1000 \
  --threshold-rules=percent=0.5,threshold-type=FORECASTED \
  --notifications-settings=email=team@example.com
```