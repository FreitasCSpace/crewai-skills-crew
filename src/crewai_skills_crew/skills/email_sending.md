# Skill: email_sending

## Purpose
Send emails programmatically via SMTP or email service APIs (SendGrid, Mailgun, AWS SES).

## When to use
- Sending notification emails or reports
- Automating email workflows
- Sending transactional emails with attachments
- Bulk email or newsletter sending

## How to execute

**Send via Python SMTP (Gmail, Outlook, any SMTP):**
```bash
python3 -c "
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
smtp_port = int(os.environ.get('SMTP_PORT', '587'))
smtp_user = os.environ['SMTP_USER']
smtp_pass = os.environ['SMTP_PASS']

msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Automated Report'

body = '''Hello,

This is an automated email with your report attached.

Best regards,
Automation Crew
'''
msg.attach(MIMEText(body, 'plain'))

# Attach a file
from email.mime.base import MIMEBase
from email import encoders
import os.path

attach_path = './output/report.md'
if os.path.exists(attach_path):
    with open(attach_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename=report.md')
    msg.attach(part)

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.send_message(msg)
    print('Email sent successfully')
"
```

**Send via SendGrid API:**
```bash
curl -s -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{"to": [{"email": "recipient@example.com"}]}],
    "from": {"email": "sender@example.com", "name": "Automation"},
    "subject": "Task Complete",
    "content": [{"type": "text/plain", "value": "Your task has been completed successfully."}]
  }'
echo ""
```

**Send HTML email via SendGrid:**
```bash
curl -s -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{"to": [{"email": "recipient@example.com"}]}],
    "from": {"email": "sender@example.com"},
    "subject": "Weekly Report",
    "content": [
      {"type": "text/html", "value": "<h1>Report</h1><p>All tasks completed.</p><table border=\"1\"><tr><th>Task</th><th>Status</th></tr><tr><td>Data collection</td><td>Done</td></tr></table>"}
    ]
  }'
```

**Send via Mailgun:**
```bash
curl -s -X POST \
  "https://api.mailgun.net/v3/$MAILGUN_DOMAIN/messages" \
  -u "api:$MAILGUN_API_KEY" \
  -F from="Automation <noreply@$MAILGUN_DOMAIN>" \
  -F to="recipient@example.com" \
  -F subject="Notification" \
  -F text="Your process is complete."
```

**Send via AWS SES:**
```bash
aws ses send-email \
  --from "sender@example.com" \
  --destination "ToAddresses=recipient@example.com" \
  --message "Subject={Data='Task Report'},Body={Text={Data='Task completed successfully.'}}" \
  --region us-east-1
```

**Send with Python (SendGrid library):**
```bash
pip install sendgrid --quiet && python3 -c "
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
import base64

message = Mail(
    from_email='sender@example.com',
    to_emails='recipient@example.com',
    subject='Report with Attachment',
    html_content='<h2>Report</h2><p>See attachment.</p>'
)

# Attach file
with open('./output/report.md', 'rb') as f:
    encoded = base64.b64encode(f.read()).decode()
message.attachment = Attachment(
    FileContent(encoded),
    FileName('report.md'),
    FileType('text/markdown')
)

sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
response = sg.send(message)
print(f'Status: {response.status_code}')
"
```

## Environment variables needed
- **SMTP**: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`
- **SendGrid**: `SENDGRID_API_KEY`
- **Mailgun**: `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`
- **AWS SES**: AWS credentials configured

## Output contract
- stdout: confirmation or API response
- HTTP 202 (SendGrid): accepted for delivery
- HTTP 200 (Mailgun): sent
- exit_code 0: success
- exit_code 1: auth error, invalid recipient, or connection failure

## Evaluate output
If "Unauthorized": check API key.
If SMTP auth fails: for Gmail, use App Password (not regular password).
If emails don't arrive: check spam folder, verify sender domain is authenticated (SPF/DKIM).
