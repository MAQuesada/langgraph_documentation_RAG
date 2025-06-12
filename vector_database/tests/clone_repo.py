# testing the cloning of repo
from vector_database.src.documentation_loader import clone_repo
import yaml

with open("vector_database/src/config.yaml") as f:
    config = yaml.safe_load(f)


clone_repo(config)
print("Clone Completed!")
