import json, os
from collections import defaultdict
from pathlib import Path

class ReportGenerator:
    def run(self):
        # Load data and pre-map images to their app/env locations
        mapping = json.load(open("results/mapping.json"))
        img_to_locs = defaultdict(list)
        for m in mapping:
            img_to_locs[m["image"]].append((m["app"], m["env"]))

        images = Path("results/images.txt").read_text().splitlines()
        report = defaultdict(lambda: defaultdict(lambda: {"critical": 0, "high": 0, "images": set()}))
        totals = {"CRITICAL": 0, "HIGH": 0}

        for i, image in enumerate(images):
            path = Path(f"results/raw/scan_{i}.json")
            if not path.exists(): continue
            
            data = json.load(path.open())
            # Flatten vulnerabilities and count severities
            vulns = [v.get("Severity") for r in data.get("Results", []) for v in (r.get("Vulnerabilities") or [])]
            counts = {sev: vulns.count(sev) for sev in ["CRITICAL", "HIGH"]}

            for app, env in img_to_locs.get(image, []):
                report[app][env]["critical"] += counts["CRITICAL"]
                report[app][env]["high"] += counts["HIGH"]
                report[app][env]["images"].add(image)

            totals["CRITICAL"] += counts["CRITICAL"]
            totals["HIGH"] += counts["HIGH"]

        final = {a: {e: {**d, "images": list(d["images"])} for e, d in envs.items()} for a, envs in report.items()}
        json.dump(final, open("results/final_report.json", "w"), indent=2)

        for app, envs in final.items():
            print(f"APP: {app}")
            for env, d in envs.items():
                print(f"  ENV: {env}\n    Critical: {d['critical']}\n    High: {d['high']}")
                for img in d["images"]: print(f"      - {img}")

        print(f"\nTOTAL CRITICAL: {totals['CRITICAL']}\nTOTAL HIGH: {totals['HIGH']}")

if __name__ == "__main__":
    ReportGenerator().run()