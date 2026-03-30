import os
import json
import logging
import sys
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrivyReportProcessor:
    def __init__(self, results_dir="results", fail_on_critical=True):
        self.results_dir = results_dir
        self.raw_dir = f"{results_dir}/raw"
        self.mapping_file = f"{results_dir}/mapping.json"
        self.output_file = f"{results_dir}/final_report.json"
        self.fail_on_critical = fail_on_critical

        self.mapping = []
        self.results = {}

    def load_mapping(self):
        with open(self.mapping_file) as f:
            self.mapping = json.load(f)

    def count(self, data):
        c = h = 0
        for r in data.get("Results", []):
            for v in r.get("Vulnerabilities", []) or []:
                if v["Severity"] == "CRITICAL":
                    c += 1
                elif v["Severity"] == "HIGH":
                    h += 1
        return c, h

    def process(self):
        images = set(item["image"] for item in self.mapping)

        for img in images:
            file_hash = os.popen(f"echo -n '{img}' | sha256sum").read().split()[0][:16]
            path = f"{self.raw_dir}/{file_hash}.json"

            if not os.path.exists(path):
                logger.warning(f"Missing scan: {img}")
                self.results[img] = {"critical": -1, "high": -1}
                continue

            try:
                with open(path) as f:
                    data = json.load(f)

                if data.get("error"):
                    raise Exception("Scan failed")

                c, h = self.count(data)
                self.results[img] = {"critical": c, "high": h}

            except Exception as e:
                logger.error(f"Failed processing {img}: {e}")
                self.results[img] = {"critical": -1, "high": -1}

    def generate(self):
        report = defaultdict(lambda: defaultdict(lambda: {
            "critical": 0,
            "high": 0,
            "images": []
        }))

        total_c = total_h = 0

        for item in self.mapping:
            app, env, img = item["app"], item["env"], item["image"]
            res = self.results.get(img, {"critical": 0, "high": 0})

            if res["critical"] == -1:
                continue

            report[app][env]["critical"] += res["critical"]
            report[app][env]["high"] += res["high"]

            total_c += res["critical"]
            total_h += res["high"]

            if img not in report[app][env]["images"]:
                report[app][env]["images"].append(img)

        logger.info(f"Total Critical: {total_c}")
        logger.info(f"Total High: {total_h}")

        if self.fail_on_critical and total_c > 0:
            logger.error("Critical vulnerabilities found! Failing pipeline.")
            sys.exit(1)

        return report

    def run(self):
        self.load_mapping()
        self.process()
        report = self.generate()

        with open(self.output_file, "w") as f:
            json.dump(report, f, indent=2)

        logger.info("Report generated")


if __name__ == "__main__":
    TrivyReportProcessor().run()