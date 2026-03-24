# Skill: azure_cli

## Purpose
Manage Azure cloud resources using the `az` CLI — VMs, storage, app services, databases, networking, and more.

## When to use
- Provisioning or managing Azure resources (VMs, Storage, App Service, AKS, SQL)
- Deploying applications to Azure
- Querying resource status, costs, or configurations
- Managing Azure AD users, groups, or role assignments
- Working with Azure Key Vault secrets

## Prerequisites
- `az` CLI installed: `brew install azure-cli` or `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
- Logged in: `az login` (or service principal: `az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID`)

**Verify:**
```bash
az --version && az account show --query "{name:name, id:id, tenantId:tenantId}" -o table
```

## How to execute

**List subscriptions:**
```bash
az account list --query "[].{Name:name, ID:id, State:state}" -o table
```

**Set active subscription:**
```bash
az account set --subscription "SUBSCRIPTION_ID"
```

**Resource Groups:**
```bash
# List
az group list --query "[].{Name:name, Location:location}" -o table

# Create
az group create --name my-rg --location eastus
```

**Virtual Machines:**
```bash
# List VMs
az vm list -g my-rg --query "[].{Name:name, State:powerState, Size:hardwareProfile.vmSize}" -o table

# Create a VM
az vm create -g my-rg -n my-vm \
  --image Ubuntu2204 --size Standard_B2s \
  --admin-username azureuser --generate-ssh-keys

# Start / Stop / Deallocate
az vm start -g my-rg -n my-vm
az vm stop -g my-rg -n my-vm
az vm deallocate -g my-rg -n my-vm
```

**App Service (Web Apps):**
```bash
# Create an App Service plan + web app
az appservice plan create -g my-rg -n my-plan --sku B1 --is-linux
az webapp create -g my-rg -p my-plan -n my-webapp --runtime "PYTHON:3.11"

# Deploy from GitHub
az webapp deployment source config -g my-rg -n my-webapp \
  --repo-url https://github.com/OWNER/REPO --branch main --manual-integration

# View logs
az webapp log tail -g my-rg -n my-webapp
```

**Storage Accounts:**
```bash
# Create
az storage account create -g my-rg -n mystorageacct --sku Standard_LRS --location eastus

# Upload a file to blob
az storage blob upload --account-name mystorageacct \
  --container-name mycontainer --name myfile.txt --file ./myfile.txt --auth-mode login

# List blobs
az storage blob list --account-name mystorageacct --container-name mycontainer -o table
```

**Azure SQL:**
```bash
# Create server + database
az sql server create -g my-rg -n my-sql-server -u sqladmin -p 'P@ssw0rd!' --location eastus
az sql db create -g my-rg -s my-sql-server -n mydb --service-objective S0
```

**AKS (Kubernetes):**
```bash
# Create cluster
az aks create -g my-rg -n my-aks --node-count 2 --generate-ssh-keys

# Get credentials
az aks get-credentials -g my-rg -n my-aks

# List nodes
kubectl get nodes
```

**Key Vault:**
```bash
# Create vault
az keyvault create -g my-rg -n my-vault --location eastus

# Set and get a secret
az keyvault secret set --vault-name my-vault --name "api-key" --value "secret123"
az keyvault secret show --vault-name my-vault --name "api-key" --query value -o tsv
```

**Azure Functions:**
```bash
# Create function app
az functionapp create -g my-rg -n my-func \
  --storage-account mystorageacct --runtime python --runtime-version 3.11 \
  --functions-version 4 --os-type Linux --consumption-plan-location eastus
```

**Cost / Billing:**
```bash
az consumption usage list --start-date 2024-01-01 --end-date 2024-01-31 \
  --query "[].{Resource:instanceName, Cost:pretaxCost, Currency:currency}" -o table
```

## Output contract
- stdout: command output (table, JSON, or TSV depending on -o flag)
- exit_code 0: success
- exit_code 1+: auth error, resource not found, or invalid params

## Evaluate output
If "Please run 'az login'": credentials expired, re-authenticate.
If "ResourceNotFound": check resource group and resource name spelling.
Always use `--query` with JMESPath to filter large outputs.
