import os, json


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
        images = [line.strip() for line in open("results/images.txt") if line.strip()]

        total_c = total_h = 0
        report = []

        for i, image in enumerate(images):
            path = f"results/raw/scan_{i}.json"

            if not os.path.exists(path):
                continue

            data = json.load(open(path))
            if data.get("error"):
                continue

            c, h = self.count(data)

            report.append({
                "image": image,
                "critical": c,
                "high": h
            })

            total_c += c
            total_h += h

        json.dump(report, open("results/final_report.json", "w"), indent=2)

        for r in report:
            print(f"{r['image']}")
            print(f"  Critical: {r['critical']}")
            print(f"  High    : {r['high']}\n")

        print(f"TOTAL CRITICAL: {total_c}")
        print(f"TOTAL HIGH    : {total_h}")


if __name__ == "__main__":
    ReportGenerator().run()