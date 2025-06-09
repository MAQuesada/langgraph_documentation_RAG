import yaml
import os
import re
from dotenv import load_dotenv

def load_config(config_path="config.yaml"):
    """
    Load configuration from a YAML file and parses environment variables.

    Args:
        config_path (str): Path to the configuration file (default is "config.yaml").

    Returns:
        dict: Parsed configuration dictionary.
    """

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    
    load_dotenv()


    def _expand_env_vars(obj):

        if isinstance(obj, dict):
            return {k : _expand_env_vars(v) for k, v in obj.items()}
        
        elif isinstance(obj, list):
            return [_expand_env_vars(i) for i in obj]
        
        elif isinstance(obj, str):

            return re.sub(r"\$\{([^}^{]+\}", lambda m: os.getenv(m.group(1), m.group(0)), obj)
        else:
            return obj

    with open(config_path, 'r') as file:
        try:
            raw_config = yaml.safe_load(file)
            return _expand_env_vars(raw_config)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")


