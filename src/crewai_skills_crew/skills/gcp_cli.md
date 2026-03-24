# Skill: gcp_cli

## Purpose
Manage Google Cloud Platform resources using the `gcloud` CLI — Compute, Storage, Cloud Run, BigQuery, and more.

## When to use
- Provisioning or managing GCP resources
- Deploying to Cloud Run, App Engine, or GKE
- Managing Cloud Storage (GCS) buckets and objects
- Running BigQuery queries
- Managing IAM and service accounts

## Prerequisites
- `gcloud` CLI installed: `brew install --cask google-cloud-sdk`
- Authenticated: `gcloud auth login` or service account: `gcloud auth activate-service-account --key-file=sa.json`
- Project set: `gcloud config set project PROJECT_ID`

**Verify:**
```bash
gcloud --version && gcloud config list --format="text(core.project,core.account)"
```

## How to execute

**List projects:**
```bash
gcloud projects list --format="table(projectId, name, projectNumber)"
```

**Cloud Storage (GCS):**
```bash
# List buckets
gcloud storage ls

# Upload a file
gcloud storage cp ./output/report.md gs://my-bucket/reports/

# Download a file
gcloud storage cp gs://my-bucket/data/input.json ./data/

# Sync a directory
gcloud storage rsync ./output/ gs://my-bucket/output/ --recursive

# List objects
gcloud storage ls gs://my-bucket/reports/ --long
```

**Compute Engine (VMs):**
```bash
# List instances
gcloud compute instances list --format="table(name, zone, status, networkInterfaces[0].accessConfigs[0].natIP)"

# Create a VM
gcloud compute instances create my-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-12 \
  --image-project=debian-cloud

# SSH into a VM
gcloud compute ssh my-vm --zone=us-central1-a

# Stop / Start
gcloud compute instances stop my-vm --zone=us-central1-a
gcloud compute instances start my-vm --zone=us-central1-a
```

**Cloud Run (serverless containers):**
```bash
# Deploy from source
gcloud run deploy my-service \
  --source . \
  --region us-central1 \
  --allow-unauthenticated

# Deploy from image
gcloud run deploy my-service \
  --image gcr.io/PROJECT_ID/my-image:latest \
  --region us-central1 \
  --set-env-vars "API_KEY=xxx,DB_URL=yyy"

# List services
gcloud run services list --format="table(name, region, status.url)"

# View logs
gcloud run services logs read my-service --region us-central1 --limit 50
```

**BigQuery:**
```bash
# Run a SQL query
bq query --use_legacy_sql=false \
  'SELECT name, COUNT(*) as count FROM `project.dataset.table` GROUP BY name ORDER BY count DESC LIMIT 10'

# List datasets
bq ls

# List tables in a dataset
bq ls project:dataset

# Export table to GCS
bq extract --destination_format CSV project:dataset.table gs://my-bucket/export/data.csv
```

**Cloud Functions:**
```bash
# Deploy a Python function
gcloud functions deploy my-function \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handler \
  --source .

# List functions
gcloud functions list

# Invoke
gcloud functions call my-function --data '{"key": "value"}'
```

**IAM & Service Accounts:**
```bash
# List service accounts
gcloud iam service-accounts list

# Create service account
gcloud iam service-accounts create my-sa --display-name "My Service Account"

# Grant role
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:my-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"
```

**Secret Manager:**
```bash
# Create a secret
echo -n "my-secret-value" | gcloud secrets create my-secret --data-file=-

# Access a secret
gcloud secrets versions access latest --secret=my-secret
```

**Container Registry / Artifact Registry:**
```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/my-image:latest

# Or with Artifact Registry
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/REPO/my-image:latest
```

## Output contract
- stdout: command output (table, JSON, or text based on --format)
- exit_code 0: success
- exit_code 1+: auth error, resource not found, or invalid params

## Evaluate output
If "Please run gcloud auth login": credentials expired.
If "ERROR: (gcloud) unrecognized arguments": check command syntax.
Use `--format=json` for machine-readable output, `--format=table` for human-readable.
Always verify the active project with `gcloud config get-value project`.
