from pathlib import Path
import yaml
from .models import Knowledge


class KnowledgeLoader:
    """
    Loads knowledge files based on manifest.yaml

    knowledge/
      v1/
        manifest.yaml
        taxonomy.yaml
        synonyms.yaml
        ...
    """

    def __init__(self, directory):
        self.directory = Path(directory)

    def load(self):

        manifest_file = self.directory / "manifest.yaml"

        if not manifest_file.exists():
            raise FileNotFoundError(
                f"manifest.yaml not found: {manifest_file}"
            )

        with open(manifest_file, "r", encoding="utf-8") as fp:
            manifest = yaml.safe_load(fp) or {}

        files = manifest.get("files", {})

        if not files:
            raise ValueError("manifest.yaml does not contain a 'files' section.")

        knowledge = Knowledge()

        for logical_name, filename in files.items():

            yaml_file = self.directory / filename

            if not yaml_file.exists():
                raise FileNotFoundError(
                    f"Knowledge file missing: {yaml_file}"
                )

            with open(yaml_file, "r", encoding="utf-8") as fp:
                knowledge.documents[logical_name] = yaml.safe_load(fp) or {}

        knowledge.documents["_manifest"] = manifest

        return knowledge
