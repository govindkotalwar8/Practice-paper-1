import os
import json
import yaml
import subprocess
import tempfile
import shutil
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

RESULTS_DIR = "results"
DEPLOYMENTS_DIR = "deployments"


# =========================
# STEP 1: EXTRACT IMAGES
# =========================
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


# =========================
# STEP 2: SCAN IMAGES
# =========================
def scan_image(image):
    cache_dir = tempfile.mkdtemp()

    cmd = [
        "trivy", "image",
        "--format", "json",
        "--severity", "HIGH,CRITICAL",
        "--scanners", "vuln",     # faster + avoids secret scanning
        "--cache-dir", cache_dir, # isolate cache to avoid lock issues
        image
    ]

    try:
        print(f"[DEBUG] Scanning: {image}")

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if res.returncode != 0:
            print(f"[ERROR] Scan failed for {image}")
            print(res.stderr.strip())
            return image, {"critical": -1, "high": -1}

        if not res.stdout.strip():
            print(f"[WARNING] Empty result for {image}")
            return image, {"critical": 0, "high": 0}

        data = json.loads(res.stdout)

        critical, high = 0, 0
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []):
                if v.get("Severity") == "CRITICAL":
                    critical += 1
                elif v.get("Severity") == "HIGH":
                    high += 1

        return image, {"critical": critical, "high": high}

    except subprocess.TimeoutExpired:
        print(f"[ERROR] Timeout while scanning {image}")
        return image, {"critical": -1, "high": -1}

    except Exception as e:
        print(f"[ERROR] Exception for {image}: {e}")
        return image, {"critical": -1, "high": -1}

    finally:
        shutil.rmtree(cache_dir, ignore_errors=True)


def scan_images(images):
    results = {}

    # safer concurrency for CI
    with ThreadPoolExecutor(max_workers=3) as executor:
        for image, result in executor.map(scan_image, images):
            results[image] = result

    return results


# =========================
# STEP 3: REPORT
# =========================
def generate_report(mapping, scan_results):
    report = defaultdict(lambda: defaultdict(lambda: {
        "critical": 0,
        "high": 0,
        "images": []
    }))

    for item in mapping:
        app, env, img = item["app"], item["env"], item["image"]
        res = scan_results.get(img, {"critical": 0, "high": 0})

        # skip failed scans
        if res["critical"] == -1:
            continue

        report[app][env]["critical"] += res["critical"]
        report[app][env]["high"] += res["high"]

        if img not in report[app][env]["images"]:
            report[app][env]["images"].append(img)

    return report


# =========================
# MAIN
# =========================
def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # ---- Extract ----
    print("[INFO] Extracting images...")
    mapping, images = get_images()

    if not images:
        print("[INFO] No images found")
        return

    print(f"[INFO] Found {len(images)} images:\n")
    for img in images:
        print(f"  - {img}")

    # ---- Scan ----
    print("\n[INFO] Scanning images...")
    scans = scan_images(images)

    # ---- Results ----
    print("\n[INFO] Scan Results:")
    for img, res in scans.items():
        if res["critical"] == -1:
            print(f"  - {img} | ❌ SCAN FAILED")
        else:
            print(f"  - {img} | CRITICAL: {res['critical']} | HIGH: {res['high']}")

    # ---- Failed ----
    failed = [img for img, res in scans.items() if res["critical"] == -1]

    if failed:
        print("\n[WARNING] Failed Scans:")
        for f in failed:
            print(f"  - {f}")

    # ---- Report ----
    print("\n[INFO] Generating report...")
    report = generate_report(mapping, scans)

    with open(f"{RESULTS_DIR}/final_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n[INFO] Final Report:\n")
    print(json.dumps(report, indent=2))

    print("\n[INFO] Done!")


if __name__ == "__main__":
    main()