# Video Recording

Capture browser automation sessions as video for debugging, documentation, or verification.

## Basic Recording

```bash
# Start recording
360browser_agent record start ./demo.webm

# Perform actions
360browser_agent open https://example.com
360browser_agent snapshot -i
360browser_agent click @e1
360browser_agent fill @e2 "test input"

# Stop and save
360browser_agent record stop
```

## Recording Commands

```bash
# Start recording to file
360browser_agent record start ./output.webm

# Stop current recording
360browser_agent record stop

# Restart with new file (stops current + starts new)
360browser_agent record restart ./take2.webm
```

## Use Cases

### Debugging Failed Automation

```bash
#!/bin/bash
# Record automation for debugging

360browser_agent record start ./debug-$(date +%Y%m%d-%H%M%S).webm

# Run your automation
360browser_agent open https://app.example.com
360browser_agent snapshot -i
360browser_agent click @e1 || {
    echo "Click failed - check recording"
    360browser_agent record stop
    exit 1
}

360browser_agent record stop
```

### Documentation Generation

```bash
#!/bin/bash
# Record workflow for documentation

360browser_agent record start ./docs/how-to-login.webm

360browser_agent open https://app.example.com/login
360browser_agent wait 1000  # Pause for visibility

360browser_agent snapshot -i
360browser_agent fill @e1 "demo@example.com"
360browser_agent wait 500

360browser_agent fill @e2 "password"
360browser_agent wait 500

360browser_agent click @e3
360browser_agent wait --load networkidle
360browser_agent wait 1000  # Show result

360browser_agent record stop
```

### CI/CD Test Evidence

```bash
#!/bin/bash
# Record E2E test runs for CI artifacts

TEST_NAME="${1:-e2e-test}"
RECORDING_DIR="./test-recordings"
mkdir -p "$RECORDING_DIR"

360browser_agent record start "$RECORDING_DIR/$TEST_NAME-$(date +%s).webm"

# Run test
if run_e2e_test; then
    echo "Test passed"
else
    echo "Test failed - recording saved"
fi

360browser_agent record stop
```

## Best Practices

### 1. Add Pauses for Clarity

```bash
# Slow down for human viewing
360browser_agent click @e1
360browser_agent wait 500  # Let viewer see result
```

### 2. Use Descriptive Filenames

```bash
# Include context in filename
360browser_agent record start ./recordings/login-flow-2024-01-15.webm
360browser_agent record start ./recordings/checkout-test-run-42.webm
```

### 3. Handle Recording in Error Cases

```bash
#!/bin/bash
set -e

cleanup() {
    360browser_agent record stop 2>/dev/null || true
    360browser_agent close 2>/dev/null || true
}
trap cleanup EXIT

360browser_agent record start ./automation.webm
# ... automation steps ...
```

### 4. Combine with Screenshots

```bash
# Record video AND capture key frames
360browser_agent record start ./flow.webm

360browser_agent open https://example.com
360browser_agent screenshot ./screenshots/step1-homepage.png

360browser_agent click @e1
360browser_agent screenshot ./screenshots/step2-after-click.png

360browser_agent record stop
```

## Output Format

- Default format: WebM (VP8/VP9 codec)
- Compatible with all modern browsers and video players
- Compressed but high quality

## Limitations

- Recording adds slight overhead to automation
- Large recordings can consume significant disk space
- Some headless environments may have codec limitations
