from git import Repo
import os

def clone_repo(config):
    url = config["data_source"]["github"]["clone_url"]
    path = config["data_source"]["github"]["target_path"]
    if not os.path.exists(path):
        Repo.clone_from(url, to_path=path, depth=1)
