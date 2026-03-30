#!/bin/bash

set -eo pipefail

RESULTS_DIR="results"
IMAGES_FILE="$RESULTS_DIR/images.txt"
RAW_DIR="$RESULTS_DIR/raw"
CACHE_DIR=".trivycache"

mkdir -p "$RAW_DIR"
mkdir -p "$CACHE_DIR"

echo "[INFO] Starting Trivy scans..."

scan_image() {
  local image="$1"
  local safe_name=$(echo "$image" | sha256sum | cut -c1-16)
  local outfile="$RAW_DIR/${safe_name}.json"

  for attempt in 1 2; do
    echo "[INFO] Scanning ($attempt): $image"

    if trivy image \
      --format json \
      --scanners vuln \
      --severity HIGH,CRITICAL \
      --cache-dir "$CACHE_DIR" \
      --skip-db-update \
      --skip-java-db-update \
      -o "$outfile" \
      "$image"; then
      return
    fi

    echo "[WARN] Retry $attempt failed for $image"
    sleep 2
  done

  echo "[ERROR] Final failure: $image"

  echo '{"error": true}' > "$outfile"
}

export -f scan_image
export RAW_DIR CACHE_DIR

cat "$IMAGES_FILE" | xargs -I {} -P 5 bash -c 'scan_image "$@"' _ {}

echo "[INFO] All scans completed"