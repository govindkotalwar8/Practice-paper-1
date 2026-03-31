images = [line.strip() for line in open("results/images.txt") if line.strip()]

lines = [
    "#!/bin/bash\n",
    "set -eo pipefail\n\n",
    "mkdir -p results/raw\n\n"
]

for i, image in enumerate(images):
    lines.append(
        f"trivy image --quiet --no-progress --format json "
        f"--scanners vuln --severity HIGH,CRITICAL "
        f"--cache-dir .trivycache_{i} "
        f"-o results/raw/scan_{i}.json {image}\n"
    )

with open("trivy_scan.sh", "w") as f:
    f.writelines(lines)