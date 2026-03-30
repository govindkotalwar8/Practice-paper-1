#!/bin/bash

set -eo pipefail

RESULTS_DIR="results"
IMAGES_FILE="$RESULTS_DIR/images.txt"
RAW_DIR="$RESULTS_DIR/raw"

mkdir -p "$RAW_DIR"

echo "[INFO] Starting Trivy scans..."

scan_image() {
  local image="$1"

  # Unique ID per image
  local hash=$(echo "$image" | sha256sum | cut -c1-12)

  local cache_dir=".trivycache_$hash"
  local outfile="$RAW_DIR/${hash}.json"

  mkdir -p "$cache_dir"

  for attempt in 1 2; do
    echo "[INFO] Scanning ($attempt): $image"

    if trivy image \
      --format json \
      --scanners vuln \
      --severity HIGH,CRITICAL \
      --cache-dir "$cache_dir" \
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

cat "$IMAGES_FILE" | xargs -I {} -P 5 bash -c 'scan_image "$@"' _ {}

echo "[INFO] All scans completed"