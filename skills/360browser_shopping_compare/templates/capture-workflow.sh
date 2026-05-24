#!/bin/bash
# Template: Content Capture Workflow
# Extract content from web pages with optional authentication

set -euo pipefail

TARGET_URL="${1:?Usage: $0 <url> [output-dir]}"
OUTPUT_DIR="${2:-.}"

echo "Capturing content from: $TARGET_URL"
mkdir -p "$OUTPUT_DIR"

# Optional: Load authentication state if needed
# if [[ -f "./auth-state.json" ]]; then
#     360browser_agent state load "./auth-state.json"
# fi

# Navigate to target page
360browser_agent open "$TARGET_URL"
360browser_agent wait --load networkidle

# Get page metadata
echo "Page title: $(360browser_agent get title)"
echo "Page URL: $(360browser_agent get url)"

# Capture full page screenshot
360browser_agent screenshot --full "$OUTPUT_DIR/page-full.png"
echo "Screenshot saved: $OUTPUT_DIR/page-full.png"

# Get page structure
360browser_agent snapshot -i > "$OUTPUT_DIR/page-structure.txt"
echo "Structure saved: $OUTPUT_DIR/page-structure.txt"

# Extract main content
# Adjust selector based on target site structure
# 360browser_agent get text @e1 > "$OUTPUT_DIR/main-content.txt"

# Extract specific elements (uncomment as needed)
# 360browser_agent get text "article" > "$OUTPUT_DIR/article.txt"
# 360browser_agent get text "main" > "$OUTPUT_DIR/main.txt"
# 360browser_agent get text ".content" > "$OUTPUT_DIR/content.txt"

# Get full page text
360browser_agent get text body > "$OUTPUT_DIR/page-text.txt"
echo "Text content saved: $OUTPUT_DIR/page-text.txt"

# Optional: Save as PDF
360browser_agent pdf "$OUTPUT_DIR/page.pdf"
echo "PDF saved: $OUTPUT_DIR/page.pdf"

# Optional: Capture with scrolling for infinite scroll pages
# scroll_and_capture() {
#     local count=0
#     while [[ $count -lt 5 ]]; do
#         360browser_agent scroll down 1000
#         360browser_agent wait 1000
#         ((count++))
#     done
#     360browser_agent screenshot --full "$OUTPUT_DIR/page-scrolled.png"
# }
# scroll_and_capture

# Cleanup
360browser_agent close

echo ""
echo "Capture complete! Files saved to: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"
