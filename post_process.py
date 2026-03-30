import os
import json
import hashlib
from collections import defaultdict


class ReportGenerator:
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        self.raw_dir = f"{results_dir}/raw"
        self.mapping_file = f"{results_dir}/mapping.json"

    def generate_hash(self, image):
        return hashlib.sha256((image + "\n").encode()).hexdigest()[:12]

    def count_vulnerabilities(self, data):
        critical = 0
        high = 0

        for result in data.get("Results", []):
            for vuln in result.get("Vulnerabilities", []) or []:
                if vuln.get("Severity") == "CRITICAL":
                    critical += 1
                elif vuln.get("Severity") == "HIGH":
                    high += 1

        return critical, high

    def run(self):
        if not os.path.exists(self.mapping_file):
            print("[ERROR] mapping.json not found")
            return

        with open(self.mapping_file) as f:
            mapping = json.load(f)

        report = defaultdict(lambda: defaultdict(lambda: {
            "critical": 0,
            "high": 0,
            "images": []
        }))

        total_critical = 0
        total_high = 0
        processed_any = False

        for item in mapping:
            app = item["app"]
            env = item["env"]
            image = item["image"]

            file_hash = self.generate_hash(image)
            file_path = f"{self.raw_dir}/{file_hash}.json"

            if not os.path.exists(file_path):
                continue

            try:
                with open(file_path) as f:
                    data = json.load(f)

                if data.get("error"):
                    continue

                c, h = self.count_vulnerabilities(data)

                report[app][env]["critical"] += c
                report[app][env]["high"] += h

                total_critical += c
                total_high += h
                processed_any = True

                if image not in report[app][env]["images"]:
                    report[app][env]["images"].append(image)

            except Exception:
                continue

        output_file = f"{self.results_dir}/final_report.json"
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)


        if not processed_any:
            print("No scan data processed\n")
        else:
            for app, envs in report.items():
                print(f"APP: {app}")
                for env, data in envs.items():
                    print(f"  ENV: {env}")
                    print(f"    Critical: {data['critical']}")
                    print(f"    High    : {data['high']}")
                    print(f"    Images  :")
                    for img in data["images"]:
                        print(f"      - {img}")
                    print()

        print(f"TOTAL CRITICAL: {total_critical}")
        print(f"TOTAL HIGH    : {total_high}")

if __name__ == "__main__":
    ReportGenerator().run()