#!/bin/bash

set -eo pipefail

RESULTS_DIR="results"
IMAGES_FILE="$RESULTS_DIR/images.txt"
RAW_DIR="$RESULTS_DIR/raw"

mkdir -p "$RAW_DIR"


scan_image() {
  local image="$1"

  local hash
  hash=$(echo "$image" | sha256sum | cut -c1-12)

  local cache_dir=".trivycache_$hash"
  local outfile="${RAW_DIR}/${hash}.json"

  mkdir -p "$cache_dir"

  for attempt in 1 2; do
    echo "[SCAN] $image (attempt $attempt)"

    if trivy image \
      --quiet \
      --no-progress \
      --format json \
      --scanners vuln \
      --severity HIGH,CRITICAL \
      --cache-dir "$cache_dir" \
      -o "$outfile" \
      "$image" >/dev/null 2>&1; then

      echo "[DONE] $image"
      return
    fi

    echo "[RETRY] $image"
    sleep 2
  done

  echo "[FAILED] $image"
  echo '{"error": true}' > "$outfile"
}

export -f scan_image
export RAW_DIR

echo "Images to scan:"
cat "$IMAGES_FILE"

xargs -a "$IMAGES_FILE" -P 5 -I {} bash -c 'scan_image "$@"' _ {}

