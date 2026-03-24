# Skill: stripe_api

## Purpose
Manage Stripe payments, customers, subscriptions, and products via the Stripe API.

## When to use
- Creating or listing customers, products, prices, subscriptions
- Processing payments or refunds
- Generating payment links or invoices
- Checking account balance or transaction history
- Automating billing workflows

## Prerequisites
- `STRIPE_SECRET_KEY` env var (starts with `sk_test_` or `sk_live_`)
- Get from https://dashboard.stripe.com/apikeys

## How to execute

**List customers:**
```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/customers?limit=10" \
  | python3 -c "
import json,sys
for c in json.load(sys.stdin)['data']:
    print(f'{c[\"id\"]:>25} {c.get(\"email\",\"N/A\"):>30} {c.get(\"name\",\"N/A\")}')"
```

**Create a customer:**
```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/customers" \
  -d "email=user@example.com" \
  -d "name=John Doe" \
  -d "metadata[company]=Acme Inc"
```

**Create a product + price:**
```bash
# Create product
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/products" \
  -d "name=Pro Plan" \
  -d "description=Full access to all features"

# Create recurring price for the product
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/prices" \
  -d "product=prod_XXXXXXX" \
  -d "unit_amount=2999" \
  -d "currency=usd" \
  -d "recurring[interval]=month"
```

**Create a subscription:**
```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/subscriptions" \
  -d "customer=cus_XXXXXXX" \
  -d "items[0][price]=price_XXXXXXX"
```

**Create a payment link:**
```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/payment_links" \
  -d "line_items[0][price]=price_XXXXXXX" \
  -d "line_items[0][quantity]=1" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['url'])"
```

**List recent charges:**
```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/charges?limit=10" \
  | python3 -c "
import json,sys
for c in json.load(sys.stdin)['data']:
    amt = c['amount']/100
    print(f'{c[\"id\"]:>30} \${amt:>8.2f} {c[\"currency\"]} {c[\"status\"]}')"
```

**Issue a refund:**
```bash
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/refunds" \
  -d "charge=ch_XXXXXXX" \
  -d "amount=500"  # $5.00 partial refund (in cents)
```

**Create an invoice:**
```bash
# Add invoice items first
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/invoiceitems" \
  -d "customer=cus_XXXXXXX" \
  -d "amount=5000" \
  -d "currency=usd" \
  -d "description=Consulting — 1 hour"

# Create and send the invoice
curl -s -X POST -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/invoices" \
  -d "customer=cus_XXXXXXX" \
  -d "auto_advance=true"
```

**Check balance:**
```bash
curl -s -u "$STRIPE_SECRET_KEY:" \
  "https://api.stripe.com/v1/balance" \
  | python3 -c "
import json,sys
b = json.load(sys.stdin)
for a in b['available']:
    print(f'Available: {a[\"amount\"]/100:.2f} {a[\"currency\"].upper()}')"
```

**List all products with prices (Python):**
```bash
pip install stripe --quiet && python3 -c "
import stripe, os
stripe.api_key = os.environ['STRIPE_SECRET_KEY']
products = stripe.Product.list(limit=20, active=True)
for p in products:
    prices = stripe.Price.list(product=p.id, active=True)
    for pr in prices:
        amt = pr.unit_amount / 100 if pr.unit_amount else 0
        interval = pr.recurring.interval if pr.recurring else 'one-time'
        print(f'{p.name:>30} | \${amt:.2f}/{interval} | {p.id}')
"
```

## Output contract
- stdout: JSON response
- HTTP 200: success
- HTTP 401: invalid API key
- HTTP 400: invalid parameters
- HTTP 402: card declined or payment failed

## Evaluate output
If 401: verify STRIPE_SECRET_KEY is set. Use test key (`sk_test_`) for development.
Amounts are in cents — multiply by 100 when creating, divide by 100 when displaying.
Always use test mode keys during development to avoid real charges.
