# Skill: terraform

## Purpose
Provision and manage cloud infrastructure as code using Terraform.

## When to use
- Creating repeatable, version-controlled infrastructure
- Managing multi-cloud resources (AWS, Azure, GCP)
- Planning and applying infrastructure changes safely
- Importing existing resources into Terraform state

## Prerequisites
- Terraform installed: `brew install terraform`
- Cloud provider credentials configured (AWS, Azure, or GCP CLI)
- Verify: `terraform --version`

## How to execute

**Initialize a project:**
```bash
mkdir -p infra && cd infra

cat > main.tf << 'EOF'
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5"
}

provider "aws" {
  region = var.region
}

variable "region" {
  default = "us-east-1"
}

variable "project" {
  default = "myproject"
}
EOF

terraform init
```

**Plan changes (dry-run):**
```bash
terraform plan -out=tfplan
```

**Apply changes:**
```bash
terraform apply tfplan
# Or without saved plan (will prompt for confirmation)
terraform apply -auto-approve
```

**Show current state:**
```bash
terraform show
terraform state list
terraform output
```

**Destroy infrastructure:**
```bash
terraform destroy -auto-approve
```

**Example — S3 bucket + DynamoDB:**
```bash
cat > storage.tf << 'EOF'
resource "aws_s3_bucket" "data" {
  bucket = "${var.project}-data-bucket"
  tags = {
    Project = var.project
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "main" {
  name         = "${var.project}-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Project = var.project
  }
}

output "bucket_name" {
  value = aws_s3_bucket.data.bucket
}
EOF
```

**Format and validate:**
```bash
terraform fmt -recursive
terraform validate
```

**Import existing resource:**
```bash
terraform import aws_s3_bucket.data my-existing-bucket
```

**Workspaces (environments):**
```bash
terraform workspace new staging
terraform workspace new production
terraform workspace select staging
terraform workspace list
```

## Output contract
- stdout: plan output, apply results, or state data
- exit_code 0: success
- exit_code 1+: config error, auth failure, or provider issue

## Evaluate output
Always run `terraform plan` before `apply` to review changes.
If "Error: No valid credential sources found": configure cloud provider CLI/env vars.
If state lock error: another apply is in progress or state is locked.
Red lines in plan = resources being destroyed — review carefully.
