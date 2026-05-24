# Authentication Patterns

Patterns for handling login flows, session persistence, and authenticated browsing.

## Basic Login Flow

```bash
# Navigate to login page
360browser_agent open https://app.example.com/login
360browser_agent wait --load networkidle

# Get form elements
360browser_agent snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Sign In"

# Fill credentials
360browser_agent fill @e1 "user@example.com"
360browser_agent fill @e2 "password123"

# Submit
360browser_agent click @e3
360browser_agent wait --load networkidle

# Verify login succeeded
360browser_agent get url  # Should be dashboard, not login
```

## Saving Authentication State

After logging in, save state for reuse:

```bash
# Login first (see above)
360browser_agent open https://app.example.com/login
360browser_agent snapshot -i
360browser_agent fill @e1 "user@example.com"
360browser_agent fill @e2 "password123"
360browser_agent click @e3
360browser_agent wait --url "**/dashboard"

# Save authenticated state
360browser_agent state save ./auth-state.json
```

## Restoring Authentication

Skip login by loading saved state:

```bash
# Load saved auth state
360browser_agent state load ./auth-state.json

# Navigate directly to protected page
360browser_agent open https://app.example.com/dashboard

# Verify authenticated
360browser_agent snapshot -i
```

## OAuth / SSO Flows

For OAuth redirects:

```bash
# Start OAuth flow
360browser_agent open https://app.example.com/auth/google

# Handle redirects automatically
360browser_agent wait --url "**/accounts.google.com**"
360browser_agent snapshot -i

# Fill Google credentials
360browser_agent fill @e1 "user@gmail.com"
360browser_agent click @e2  # Next button
360browser_agent wait 2000
360browser_agent snapshot -i
360browser_agent fill @e3 "password"
360browser_agent click @e4  # Sign in

# Wait for redirect back
360browser_agent wait --url "**/app.example.com**"
360browser_agent state save ./oauth-state.json
```

## Two-Factor Authentication

Handle 2FA with manual intervention:

```bash
# Login with credentials
360browser_agent open https://app.example.com/login --headed  # Show browser
360browser_agent snapshot -i
360browser_agent fill @e1 "user@example.com"
360browser_agent fill @e2 "password123"
360browser_agent click @e3

# Wait for user to complete 2FA manually
echo "Complete 2FA in the browser window..."
360browser_agent wait --url "**/dashboard" --timeout 120000

# Save state after 2FA
360browser_agent state save ./2fa-state.json
```

## HTTP Basic Auth

For sites using HTTP Basic Authentication:

```bash
# Set credentials before navigation
360browser_agent set credentials username password

# Navigate to protected resource
360browser_agent open https://protected.example.com/api
```

## Cookie-Based Auth

Manually set authentication cookies:

```bash
# Set auth cookie
360browser_agent cookies set session_token "abc123xyz"

# Navigate to protected page
360browser_agent open https://app.example.com/dashboard
```

## Token Refresh Handling

For sessions with expiring tokens:

```bash
#!/bin/bash
# Wrapper that handles token refresh

STATE_FILE="./auth-state.json"

# Try loading existing state
if [[ -f "$STATE_FILE" ]]; then
    360browser_agent state load "$STATE_FILE"
    360browser_agent open https://app.example.com/dashboard

    # Check if session is still valid
    URL=$(360browser_agent get url)
    if [[ "$URL" == *"/login"* ]]; then
        echo "Session expired, re-authenticating..."
        # Perform fresh login
        360browser_agent snapshot -i
        360browser_agent fill @e1 "$USERNAME"
        360browser_agent fill @e2 "$PASSWORD"
        360browser_agent click @e3
        360browser_agent wait --url "**/dashboard"
        360browser_agent state save "$STATE_FILE"
    fi
else
    # First-time login
    360browser_agent open https://app.example.com/login
    # ... login flow ...
fi
```

## Security Best Practices

1. **Never commit state files** - They contain session tokens
   ```bash
   echo "*.auth-state.json" >> .gitignore
   ```

2. **Use environment variables for credentials**
   ```bash
   360browser_agent fill @e1 "$APP_USERNAME"
   360browser_agent fill @e2 "$APP_PASSWORD"
   ```

3. **Clean up after automation**
   ```bash
   360browser_agent cookies clear
   rm -f ./auth-state.json
   ```

4. **Use short-lived sessions for CI/CD**
   ```bash
   # Don't persist state in CI
   360browser_agent open https://app.example.com/login
   # ... login and perform actions ...
   360browser_agent close  # Session ends, nothing persisted
   ```
