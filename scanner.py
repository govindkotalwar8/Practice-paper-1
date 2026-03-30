import os
import sys
import json
import yaml
from collections import defaultdict

RESULTS_DIR = "results"
DEPLOYMENTS_DIR = "deployments"


# -----------------------------
# Extract images recursively
# -----------------------------
def extract_images(data):
    images = []

    if isinstance(data, dict):
        for k, v in data.items():
            if k == "image":
                if isinstance(v, str):
                    images.append(v.strip())
                elif isinstance(v, dict):
                    repo = v.get("repository", "")
                    tag = v.get("tag", "")
                    if repo and tag:
                        images.append(f"{repo}:{tag}")
            else:
                images.extend(extract_images(v))

    elif isinstance(data, list):
        for item in data:
            images.extend(extract_images(item))

    return images


# -----------------------------
# Read deployment YAMLs
# -----------------------------
def get_images():
    mapping = []
    unique_images = set()

    for root, _, files in os.walk(DEPLOYMENTS_DIR):
        for file in files:
            if not file.endswith((".yaml", ".yml")):
                continue

            rel = os.path.relpath(root, DEPLOYMENTS_DIR).split(os.sep)
            app = rel[0] if len(rel) > 0 else "unknown"
            env = rel[1] if len(rel) > 1 else "unknown"

            path = os.path.join(root, file)

            try:
                with open(path) as f:
                    docs = yaml.safe_load_all(f)

                    for doc in docs:
                        if not doc:
                            continue

                        for img in extract_images(doc):
                            if img and img.lower() != "none":
                                mapping.append({
                                    "app": app,
                                    "env": env,
                                    "image": img
                                })
                                unique_images.add(img)

            except Exception as e:
                print(f"[ERROR] Failed parsing {path}: {e}")

    return mapping, list(unique_images)


# -----------------------------
# Save images for bash scan
# -----------------------------
def save_images_for_scan(images):
    path = f"{RESULTS_DIR}/images.txt"
    with open(path, "w") as f:
        for img in images:
            f.write(img + "\n")

    print(f"[INFO] Images saved to {path}")


# -----------------------------
# Load scan results from bash
# -----------------------------
def load_scan_results():
    path = f"{RESULTS_DIR}/scan_results.json"

    if not os.path.exists(path):
        print("[ERROR] scan_results.json not found")
        return {}

    with open(path) as f:
        return json.load(f)


# -----------------------------
# Generate final report
# -----------------------------
def generate_report(mapping, scan_results):
    report = defaultdict(lambda: defaultdict(lambda: {
        "critical": 0,
        "high": 0,
        "images": []
    }))

    for item in mapping:
        app = item["app"]
        env = item["env"]
        img = item["image"]

        res = scan_results.get(img, {"critical": 0, "high": 0})

        if res["critical"] == -1:
            continue

        report[app][env]["critical"] += res["critical"]
        report[app][env]["high"] += res["high"]

        if img not in report[app][env]["images"]:
            report[app][env]["images"].append(img)

    return report


# -----------------------------
# Main entry
# -----------------------------
def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if len(sys.argv) < 2:
        print("[ERROR] Mode required: --extract-only OR --report-only")
        sys.exit(1)

    mode = sys.argv[1]

    # -------------------------
    # Step 1: Extract Images
    # -------------------------
    if mode == "--extract-only":
        print("[INFO] Extracting images...")

        mapping, images = get_images()

        if not images:
            print("[INFO] No images found")
            return

        print(f"[INFO] Found {len(images)} images")

        save_images_for_scan(images)

        # Save mapping for later
        with open(f"{RESULTS_DIR}/mapping.json", "w") as f:
            json.dump(mapping, f, indent=2)

        print("[INFO] Mapping saved")

    # -------------------------
    # Step 2: Generate Report
    # -------------------------
    elif mode == "--report-only":
        print("[INFO] Loading mapping and scan results...")

        mapping_path = f"{RESULTS_DIR}/mapping.json"

        if not os.path.exists(mapping_path):
            print("[ERROR] mapping.json not found")
            sys.exit(1)

        with open(mapping_path) as f:
            mapping = json.load(f)

        scans = load_scan_results()

        print("[INFO] Generating report...")
        report = generate_report(mapping, scans)

        output_path = f"{RESULTS_DIR}/final_report.json"
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"[INFO] Report generated: {output_path}")

    else:
        print("[ERROR] Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    main()