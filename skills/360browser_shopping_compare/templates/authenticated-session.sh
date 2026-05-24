#!/bin/bash
# Template: Authenticated Session Workflow
# Login once, save state, reuse for subsequent runs
#
# Usage:
#   ./authenticated-session.sh <login-url> [state-file]
#
# Setup:
#   1. Run once to see your form structure
#   2. Note the @refs for your fields
#   3. Uncomment LOGIN FLOW section and update refs

set -euo pipefail

LOGIN_URL="${1:?Usage: $0 <login-url> [state-file]}"
STATE_FILE="${2:-./auth-state.json}"

echo "Authentication workflow for: $LOGIN_URL"

# ══════════════════════════════════════════════════════════════
# SAVED STATE: Skip login if we have valid saved state
# ══════════════════════════════════════════════════════════════
if [[ -f "$STATE_FILE" ]]; then
    echo "Loading saved authentication state..."
    360browser_agent state load "$STATE_FILE"
    360browser_agent open "$LOGIN_URL"
    360browser_agent wait --load networkidle

    CURRENT_URL=$(360browser_agent get url)
    if [[ "$CURRENT_URL" != *"login"* ]] && [[ "$CURRENT_URL" != *"signin"* ]]; then
        echo "Session restored successfully!"
        360browser_agent snapshot -i
        exit 0
    fi
    echo "Session expired, performing fresh login..."
    rm -f "$STATE_FILE"
fi

# ══════════════════════════════════════════════════════════════
# DISCOVERY MODE: Show form structure (remove after setup)
# ══════════════════════════════════════════════════════════════
echo "Opening login page..."
360browser_agent open "$LOGIN_URL"
360browser_agent wait --load networkidle

echo ""
echo "┌─────────────────────────────────────────────────────────┐"
echo "│ LOGIN FORM STRUCTURE                                    │"
echo "├─────────────────────────────────────────────────────────┤"
360browser_agent snapshot -i
echo "└─────────────────────────────────────────────────────────┘"
echo ""
echo "Next steps:"
echo "  1. Note refs: @e? = username, @e? = password, @e? = submit"
echo "  2. Uncomment LOGIN FLOW section below"
echo "  3. Replace @e1, @e2, @e3 with your refs"
echo "  4. Delete this DISCOVERY MODE section"
echo ""
360browser_agent close
exit 0

# ══════════════════════════════════════════════════════════════
# LOGIN FLOW: Uncomment and customize after discovery
# ══════════════════════════════════════════════════════════════
# : "${APP_USERNAME:?Set APP_USERNAME environment variable}"
# : "${APP_PASSWORD:?Set APP_PASSWORD environment variable}"
#
# 360browser_agent open "$LOGIN_URL"
# 360browser_agent wait --load networkidle
# 360browser_agent snapshot -i
#
# # Fill credentials (update refs to match your form)
# 360browser_agent fill @e1 "$APP_USERNAME"
# 360browser_agent fill @e2 "$APP_PASSWORD"
# 360browser_agent click @e3
# 360browser_agent wait --load networkidle
#
# # Verify login succeeded
# FINAL_URL=$(360browser_agent get url)
# if [[ "$FINAL_URL" == *"login"* ]] || [[ "$FINAL_URL" == *"signin"* ]]; then
#     echo "ERROR: Login failed - still on login page"
#     360browser_agent screenshot /tmp/login-failed.png
#     360browser_agent close
#     exit 1
# fi
#
# # Save state for future runs
# echo "Saving authentication state to: $STATE_FILE"
# 360browser_agent state save "$STATE_FILE"
# echo "Login successful!"
# 360browser_agent snapshot -i
