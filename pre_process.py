import os
import json
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageExtractor:
    def __init__(self, deployments_dir="deployments", results_dir="results"):
        self.deployments_dir = deployments_dir
        self.results_dir = results_dir
        self.mapping = []
        self.images = set()

    def normalize(self, img):
        return img if ":" in img else f"{img}:latest"

    def extract_images(self, data):
        images = []

        if isinstance(data, dict):
            for k, v in data.items():
                if k == "image":
                    if isinstance(v, str):
                        images.append(self.normalize(v.strip()))
                    elif isinstance(v, dict):
                        repo = v.get("repository")
                        tag = v.get("tag")
                        if repo and tag:
                            images.append(f"{repo}:{tag}")
                else:
                    images.extend(self.extract_images(v))

        elif isinstance(data, list):
            for item in data:
                images.extend(self.extract_images(item))

        return images

    def run(self):
        os.makedirs(self.results_dir, exist_ok=True)

        for root, _, files in os.walk(self.deployments_dir):
            for file in files:
                if not file.endswith((".yaml", ".yml")):
                    continue

                rel = os.path.relpath(root, self.deployments_dir).split(os.sep)
                app = rel[0] if len(rel) > 0 else "unknown"
                env = rel[1] if len(rel) > 1 else "unknown"

                path = os.path.join(root, file)

                try:
                    with open(path) as f:
                        for doc in yaml.safe_load_all(f):
                            if not doc:
                                continue

                            for img in self.extract_images(doc):
                                self.mapping.append({
                                    "app": app,
                                    "env": env,
                                    "image": img
                                })
                                self.images.add(img)

                except Exception as e:
                    logger.error(f"Failed parsing {path}: {e}")

        # Save
        with open(f"{self.results_dir}/images.txt", "w") as f:
            for img in sorted(self.images):
                f.write(img + "\n")

        with open(f"{self.results_dir}/mapping.json", "w") as f:
            json.dump(self.mapping, f, indent=2)

        logger.info(f"Extracted {len(self.images)} images")


if __name__ == "__main__":
    ImageExtractor().run()