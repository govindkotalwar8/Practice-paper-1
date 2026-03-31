import os, json, yaml


class ImageExtractor:
    def extract(self, d):
        if isinstance(d, dict):
            imgs = []
            for k, v in d.items():
                if k == "image":
                    if isinstance(v, str):
                        imgs.append(v if ":" in v else f"{v}:latest")
                    elif isinstance(v, dict) and v.get("repository") and v.get("tag"):
                        imgs.append(f"{v['repository']}:{v['tag']}")
                else:
                    imgs.extend(self.extract(v))
            return imgs

        if isinstance(d, list):
            return sum((self.extract(i) for i in d), [])

        return []

    def run(self):
        images = set()
        mapping = []

        for root, _, files in os.walk("deployments"):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    rel = os.path.relpath(root, "deployments").split(os.sep)
                    app = rel[0] if len(rel) > 0 else "unknown"
                    env = rel[1] if len(rel) > 1 else "unknown"

                    path = os.path.join(root, file)

                    for doc in yaml.safe_load_all(open(path)):
                        if doc:
                            for img in self.extract(doc):
                                images.add(img)
                                mapping.append({
                                    "app": app,
                                    "env": env,
                                    "image": img
                                })

        os.makedirs("results", exist_ok=True)

        open("results/images.txt", "w").write("\n".join(sorted(images)))
        json.dump(mapping, open("results/mapping.json", "w"), indent=2)

        print("\n".join(sorted(images)))


if __name__ == "__main__":
    ImageExtractor().run()