# Session Management

Run multiple isolated browser sessions concurrently with state persistence.

## Named Sessions

Use `--session` flag to isolate browser contexts:

```bash
# Session 1: Authentication flow
360browser_agent --session auth open https://app.example.com/login

# Session 2: Public browsing (separate cookies, storage)
360browser_agent --session public open https://example.com

# Commands are isolated by session
360browser_agent --session auth fill @e1 "user@example.com"
360browser_agent --session public get text body
```

## Session Isolation Properties

Each session has independent:
- Cookies
- LocalStorage / SessionStorage
- IndexedDB
- Cache
- Browsing history
- Open tabs

## Session State Persistence

### Save Session State

```bash
# Save cookies, storage, and auth state
360browser_agent state save /path/to/auth-state.json
```

### Load Session State

```bash
# Restore saved state
360browser_agent state load /path/to/auth-state.json

# Continue with authenticated session
360browser_agent open https://app.example.com/dashboard
```

### State File Contents

```json
{
  "cookies": [...],
  "localStorage": {...},
  "sessionStorage": {...},
  "origins": [...]
}
```

## Common Patterns

### Authenticated Session Reuse

```bash
#!/bin/bash
# Save login state once, reuse many times

STATE_FILE="/tmp/auth-state.json"

# Check if we have saved state
if [[ -f "$STATE_FILE" ]]; then
    360browser_agent state load "$STATE_FILE"
    360browser_agent open https://app.example.com/dashboard
else
    # Perform login
    360browser_agent open https://app.example.com/login
    360browser_agent snapshot -i
    360browser_agent fill @e1 "$USERNAME"
    360browser_agent fill @e2 "$PASSWORD"
    360browser_agent click @e3
    360browser_agent wait --load networkidle

    # Save for future use
    360browser_agent state save "$STATE_FILE"
fi
```

### Concurrent Scraping

```bash
#!/bin/bash
# Scrape multiple sites concurrently

# Start all sessions
360browser_agent --session site1 open https://site1.com &
360browser_agent --session site2 open https://site2.com &
360browser_agent --session site3 open https://site3.com &
wait

# Extract from each
360browser_agent --session site1 get text body > site1.txt
360browser_agent --session site2 get text body > site2.txt
360browser_agent --session site3 get text body > site3.txt

# Cleanup
360browser_agent --session site1 close
360browser_agent --session site2 close
360browser_agent --session site3 close
```

### A/B Testing Sessions

```bash
# Test different user experiences
360browser_agent --session variant-a open "https://app.com?variant=a"
360browser_agent --session variant-b open "https://app.com?variant=b"

# Compare
360browser_agent --session variant-a screenshot /tmp/variant-a.png
360browser_agent --session variant-b screenshot /tmp/variant-b.png
```

## Default Session

When `--session` is omitted, commands use the default session:

```bash
# These use the same default session
360browser_agent open https://example.com
360browser_agent snapshot -i
360browser_agent close  # Closes default session
```

## Session Cleanup

```bash
# Close specific session
360browser_agent --session auth close

# List active sessions
360browser_agent session list
```

## Best Practices

### 1. Name Sessions Semantically

```bash
# GOOD: Clear purpose
360browser_agent --session github-auth open https://github.com
360browser_agent --session docs-scrape open https://docs.example.com

# AVOID: Generic names
360browser_agent --session s1 open https://github.com
```

### 2. Always Clean Up

```bash
# Close sessions when done
360browser_agent --session auth close
360browser_agent --session scrape close
```

### 3. Handle State Files Securely

```bash
# Don't commit state files (contain auth tokens!)
echo "*.auth-state.json" >> .gitignore

# Delete after use
rm /tmp/auth-state.json
```

### 4. Timeout Long Sessions

```bash
# Set timeout for automated scripts
timeout 60 360browser_agent --session long-task get text body
```
