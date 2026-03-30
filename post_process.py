import os
import json
from collections import defaultdict


class ReportGenerator:
    def __init__(self, results_dir="results"):
        self.results_dir = results_dir
        self.raw_dir = f"{results_dir}/raw"
        self.mapping_file = f"{results_dir}/mapping.json"

    def hash(self, image):
        return os.popen(f"echo -n '{image}' | sha256sum").read().split()[0][:12]

    def count(self, data):
        c = h = 0
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []) or []:
                if v["Severity"] == "CRITICAL":
                    c += 1
                elif v["Severity"] == "HIGH":
                    h += 1
        return c, h

    def run(self):
        with open(self.mapping_file) as f:
            mapping = json.load(f)

        report = defaultdict(lambda: defaultdict(lambda: {
            "critical": 0,
            "high": 0,
            "images": []
        }))

        total_c = total_h = 0

        for item in mapping:
            img = item["image"]
            file = f"{self.raw_dir}/{self.hash(img)}.json"

            if not os.path.exists(file):
                continue

            try:
                with open(file) as f:
                    data = json.load(f)

                if data.get("error"):
                    continue

                c, h = self.count(data)

                report[item["app"]][item["env"]]["critical"] += c
                report[item["app"]][item["env"]]["high"] += h

                total_c += c
                total_h += h

                if img not in report[item["app"]][item["env"]]["images"]:
                    report[item["app"]][item["env"]]["images"].append(img)

            except:
                continue

        # Save JSON
        output = f"{self.results_dir}/final_report.json"
        with open(output, "w") as f:
            json.dump(report, f, indent=2)


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

        print(f"TOTAL CRITICAL: {total_c}")
        print(f"TOTAL HIGH    : {total_h}")


if __name__ == "__main__":
    ReportGenerator().run()