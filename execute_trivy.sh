#!/bin/bash
set -eo pipefail

RESULTS_DIR="results"
IMAGES_FILE="$RESULTS_DIR/images.txt"
RAW_DIR="$RESULTS_DIR/raw"

mkdir -p "$RAW_DIR"

i=0

while read -r image; do
  [ -z "$image" ] && continue

  echo "[SCAN] $image"

  trivy image \
    --quiet \
    --no-progress \
    --format json \
    --scanners vuln \
    --severity HIGH,CRITICAL \
    --cache-dir ".trivycache_$i" \
    -o "$RAW_DIR/scan_$i.json" \
    "$image"

  i=$((i+1))

done < "$IMAGES_FILE"

echo "Scan completed"