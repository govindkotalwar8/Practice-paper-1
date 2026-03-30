import os
import json
import yaml


class ImageExtractor:
    def __init__(self, deployments_dir="deployments", results_dir="results"):
        self.deployments_dir = deployments_dir
        self.results_dir = results_dir
        self.images = set()
        self.mapping = []

    def normalize(self, img):
        return img if ":" in img else f"{img}:latest"

    def extract(self, data):
        imgs = []

        if isinstance(data, dict):
            for k, v in data.items():
                if k == "image":
                    if isinstance(v, str):
                        imgs.append(self.normalize(v.strip()))
                    elif isinstance(v, dict):
                        repo = v.get("repository")
                        tag = v.get("tag")
                        if repo and tag:
                            imgs.append(f"{repo}:{tag}")
                else:
                    imgs.extend(self.extract(v))

        elif isinstance(data, list):
            for i in data:
                imgs.extend(self.extract(i))

        return imgs

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

                            for img in self.extract(doc):
                                self.images.add(img)
                                self.mapping.append({
                                    "app": app,
                                    "env": env,
                                    "image": img
                                })
                except Exception as e:
                    print(f"[ERROR] {path}: {e}")

        # Save files
        with open(f"{self.results_dir}/images.txt", "w") as f:
            for img in sorted(self.images):
                f.write(img + "\n")

        with open(f"{self.results_dir}/mapping.json", "w") as f:
            json.dump(self.mapping, f, indent=2)

        # 🔥 Clean print
        print("\n EXTRACTED IMAGES ")
        for img in sorted(self.images):
            print(f" - {img}")


if __name__ == "__main__":
    ImageExtractor().run()