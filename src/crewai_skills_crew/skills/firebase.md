# Skill: firebase

## Purpose
Manage Firebase projects — Firestore, Auth, Storage, Hosting, and Cloud Functions using the Firebase CLI and REST API.

## When to use
- Reading/writing Firestore documents
- Managing Firebase Authentication users
- Deploying to Firebase Hosting or Cloud Functions
- Uploading/downloading files in Firebase Storage
- Configuring Firebase project settings

## Prerequisites
- Firebase CLI: `npm install -g firebase-tools`
- Logged in: `firebase login` or use `FIREBASE_TOKEN` env var
- For REST API: `FIREBASE_PROJECT_ID` and `FIREBASE_API_KEY` or service account

**Verify:**
```bash
firebase --version && firebase projects:list
```

## How to execute

**Firestore — Read documents (REST API):**
```bash
curl -s "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/users?pageSize=10" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  | python3 -c "
import json,sys
docs = json.load(sys.stdin).get('documents',[])
for d in docs:
    name = d['name'].split('/')[-1]
    fields = {k: list(v.values())[0] for k,v in d.get('fields',{}).items()}
    print(f'{name}: {fields}')"
```

**Firestore — Write a document:**
```bash
curl -s -X PATCH \
  "https://firestore.googleapis.com/v1/projects/$FIREBASE_PROJECT_ID/databases/(default)/documents/users/user123" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "name": {"stringValue": "Alice"},
      "email": {"stringValue": "alice@example.com"},
      "age": {"integerValue": "30"}
    }
  }'
```

**Firestore via Python (recommended):**
```bash
pip install firebase-admin --quiet && python3 -c "
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Use service account key file
cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service-account.json'))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Read all docs in a collection
docs = db.collection('users').limit(10).stream()
for doc in docs:
    print(f'{doc.id}: {doc.to_dict()}')

# Write a document
db.collection('users').document('user456').set({
    'name': 'Bob',
    'email': 'bob@example.com',
    'created': firestore.SERVER_TIMESTAMP
})
print('Document written.')
"
```

**Deploy to Firebase Hosting:**
```bash
# Initialize (first time)
firebase init hosting

# Deploy
firebase deploy --only hosting
```

**Deploy Cloud Functions:**
```bash
firebase deploy --only functions
```

**Manage Auth users (REST):**
```bash
# List users (requires Admin SDK)
pip install firebase-admin --quiet && python3 -c "
import firebase_admin
from firebase_admin import auth, credentials
import os

cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service-account.json'))
firebase_admin.initialize_app(cred)

for user in auth.list_users().iterate_all():
    print(f'{user.uid}  {user.email}  {user.display_name or \"-\"}')"
```

**Firebase Storage — Upload:**
```bash
python3 -c "
import firebase_admin
from firebase_admin import credentials, storage
import os

cred = credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'service-account.json'))
app = firebase_admin.initialize_app(cred, {'storageBucket': os.environ['FIREBASE_PROJECT_ID'] + '.appspot.com'})

bucket = storage.bucket()
blob = bucket.blob('reports/report.md')
blob.upload_from_filename('./output/report.md')
print(f'Uploaded: {blob.public_url}')
"
```

**Firebase project configuration:**
```bash
# List projects
firebase projects:list

# Use a specific project
firebase use PROJECT_ID

# Get current project config
firebase apps:sdkconfig
```

## Output contract
- stdout: query results or deployment status
- exit_code 0: success
- exit_code 1+: auth error, project not found, or deployment failure

## Evaluate output
If 403 on REST: check auth token or service account permissions.
For Firestore, field values use typed wrappers (`stringValue`, `integerValue`, etc.) in REST — the Python SDK handles this automatically.
If deploy fails: check `firebase.json` configuration and ensure project is selected.
