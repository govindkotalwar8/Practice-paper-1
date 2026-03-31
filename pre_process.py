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

        for root, _, files in os.walk("deployments"):
            for file in files:
                if file.endswith((".yaml", ".yml")):
                    path = os.path.join(root, file)

                    for doc in yaml.safe_load_all(open(path)):
                        if doc:
                            images.update(self.extract(doc))

        os.makedirs("results", exist_ok=True)

        open("results/images.txt", "w").write("\n".join(sorted(images)))

        print("\n".join(sorted(images)))


if __name__ == "__main__":
    ImageExtractor().run()