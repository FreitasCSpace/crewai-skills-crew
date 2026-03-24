# Skill: aws_cli

## Purpose
Manage AWS cloud resources using the `aws` CLI — S3, EC2, Lambda, RDS, IAM, CloudFormation, and more.

## When to use
- Provisioning or managing AWS infrastructure
- Uploading/downloading files to S3
- Deploying Lambda functions
- Managing EC2 instances, RDS databases, or ECS services
- Querying IAM users, roles, or policies

## Prerequisites
- AWS CLI installed: `pip install awscli` or `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip && unzip awscliv2.zip && ./aws/install`
- Configured: `aws configure` (or env vars `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`)

**Verify:**
```bash
aws --version && aws sts get-caller-identity
```

## How to execute

**S3 — Buckets and Objects:**
```bash
# List buckets
aws s3 ls

# Upload a file
aws s3 cp ./output/report.md s3://my-bucket/reports/report.md

# Download a file
aws s3 cp s3://my-bucket/data/input.json ./data/input.json

# Sync a directory
aws s3 sync ./output/ s3://my-bucket/output/ --delete

# List objects in a bucket
aws s3 ls s3://my-bucket/reports/ --recursive --human-readable
```

**EC2 — Instances:**
```bash
# List running instances
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,IP:PublicIpAddress,Name:Tags[?Key=='Name']|[0].Value}" \
  --output table

# Start / Stop
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0

# Launch an instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-12345 \
  --subnet-id subnet-12345 \
  --count 1 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=my-server}]'
```

**Lambda:**
```bash
# List functions
aws lambda list-functions --query "Functions[].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize}" --output table

# Invoke a function
aws lambda invoke --function-name my-function \
  --payload '{"key": "value"}' \
  --cli-binary-format raw-in-base64-out \
  output.json && cat output.json

# Update function code from zip
zip -r function.zip . -x '*.git*'
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

**RDS:**
```bash
# List databases
aws rds describe-db-instances \
  --query "DBInstances[].{ID:DBInstanceIdentifier,Engine:Engine,Status:DBInstanceStatus,Endpoint:Endpoint.Address}" \
  --output table
```

**IAM:**
```bash
# List users
aws iam list-users --query "Users[].{Name:UserName,Created:CreateDate}" --output table

# List roles
aws iam list-roles --query "Roles[].{Name:RoleName,Arn:Arn}" --output table
```

**CloudFormation:**
```bash
# Deploy a stack
aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name my-stack \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides Env=prod

# List stacks
aws cloudformation list-stacks --query "StackSummaries[?StackStatus!='DELETE_COMPLETE'].{Name:StackName,Status:StackStatus}" --output table
```

**ECS:**
```bash
# List clusters
aws ecs list-clusters

# List services in a cluster
aws ecs list-services --cluster my-cluster

# Update service (force new deployment)
aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

**Secrets Manager:**
```bash
# Get a secret
aws secretsmanager get-secret-value --secret-id my-secret --query SecretString --output text
```

## Output contract
- stdout: command output (JSON, table, or text depending on --output flag)
- exit_code 0: success
- exit_code 1+: auth error, resource not found, or invalid params

## Evaluate output
If "Unable to locate credentials": run `aws configure` or set env vars.
If "AccessDenied": check IAM permissions for the operation.
Always use `--query` (JMESPath) and `--output table` to keep output readable.
