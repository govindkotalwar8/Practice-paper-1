#!/bin/bash

set -e

RESULTS_DIR="results"
IMAGES_FILE="$RESULTS_DIR/images.txt"
OUTPUT_FILE="$RESULTS_DIR/scan_results.json"

echo "[INFO] Starting Trivy scans..."

if [ ! -f "$IMAGES_FILE" ]; then
  echo "[ERROR] images.txt not found!"
  exit 1
fi

# Initialize JSON
TMP_FILE=$(mktemp)
echo "{}" > "$TMP_FILE"

while read -r image; do
  [ -z "$image" ] && continue

  echo "[DEBUG] Scanning: $image"

  result=$(trivy image \
    --format json \
    --severity HIGH,CRITICAL \
    --scanners vuln \
    "$image" 2>/dev/null)

  if [ $? -ne 0 ] || [ -z "$result" ]; then
    echo "[ERROR] Scan failed for $image"

    jq --arg img "$image" \
       '.[$img] = {"critical": -1, "high": -1}' \
       "$TMP_FILE" > tmp.json && mv tmp.json "$TMP_FILE"

    continue
  fi

  critical=$(echo "$result" | jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length')
  high=$(echo "$result" | jq '[.Results[].Vulnerabilities[]? | select(.Severity=="HIGH")] | length')

  jq --arg img "$image" \
     --argjson c "$critical" \
     --argjson h "$high" \
     '.[$img] = {"critical": $c, "high": $h}' \
     "$TMP_FILE" > tmp.json && mv tmp.json "$TMP_FILE"

done < "$IMAGES_FILE"

mv "$TMP_FILE" "$OUTPUT_FILE"

echo "[INFO] Scan completed."
echo "[INFO] Results saved to $OUTPUT_FILE"