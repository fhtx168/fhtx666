#!/bin/bash
# Template: Form Automation Workflow
# Fills and submits web forms with validation

set -euo pipefail

FORM_URL="${1:?Usage: $0 <form-url>}"

echo "Automating form at: $FORM_URL"

# Navigate to form page
360browser_agent open "$FORM_URL"
360browser_agent wait --load networkidle

# Get interactive snapshot to identify form fields
echo "Analyzing form structure..."
360browser_agent snapshot -i

# Example: Fill common form fields
# Uncomment and modify refs based on snapshot output

# Text inputs
# 360browser_agent fill @e1 "John Doe"           # Name field
# 360browser_agent fill @e2 "user@example.com"   # Email field
# 360browser_agent fill @e3 "+1-555-123-4567"    # Phone field

# Password fields
# 360browser_agent fill @e4 "SecureP@ssw0rd!"

# Dropdowns
# 360browser_agent select @e5 "Option Value"

# Checkboxes
# 360browser_agent check @e6                      # Check
# 360browser_agent uncheck @e7                    # Uncheck

# Radio buttons
# 360browser_agent click @e8                      # Select radio option

# Text areas
# 360browser_agent fill @e9 "Multi-line text content here"

# File uploads
# 360browser_agent upload @e10 /path/to/file.pdf

# Submit form
# 360browser_agent click @e11                     # Submit button

# Wait for response
# 360browser_agent wait --load networkidle
# 360browser_agent wait --url "**/success"        # Or wait for redirect

# Verify submission
echo "Form submission result:"
360browser_agent get url
360browser_agent snapshot -i

# Take screenshot of result
360browser_agent screenshot /tmp/form-result.png

# Cleanup
360browser_agent close

echo "Form automation complete"
