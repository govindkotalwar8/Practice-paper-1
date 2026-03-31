import os, json
from collections import defaultdict


class ReportGenerator:
    def count(self, data):
        c = h = 0
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []) or []:
                if v.get("Severity") == "CRITICAL":
                    c += 1
                elif v.get("Severity") == "HIGH":
                    h += 1
        return c, h

    def run(self):
        mapping = json.load(open("results/mapping.json"))
        images = [line.strip() for line in open("results/images.txt") if line.strip()]

        report = defaultdict(lambda: defaultdict(lambda: {
            "critical": 0,
            "high": 0,
            "images": []
        }))

        total_c = total_h = 0

        for i, image in enumerate(images):
            path = f"results/raw/scan_{i}.json"
            if not os.path.exists(path):
                continue

            data = json.load(open(path))
            if data.get("error"):
                continue

            c, h = self.count(data)

            # map image → app/env
            for m in mapping:
                if m["image"] == image:
                    app, env = m["app"], m["env"]

                    report[app][env]["critical"] += c
                    report[app][env]["high"] += h

                    if image not in report[app][env]["images"]:
                        report[app][env]["images"].append(image)

            total_c += c
            total_h += h

        json.dump(report, open("results/final_report.json", "w"), indent=2)

        for app in report:
            print(f"APP: {app}")
            for env in report[app]:
                d = report[app][env]
                print(f"  ENV: {env}")
                print(f"    Critical: {d['critical']}")
                print(f"    High    : {d['high']}")
                for img in d["images"]:
                    print(f"      - {img}")
                print()

        print(f"TOTAL CRITICAL: {total_c}")
        print(f"TOTAL HIGH    : {total_h}")


if __name__ == "__main__":
    ReportGenerator().run()