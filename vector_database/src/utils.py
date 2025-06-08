import yaml
import os

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
    
    with open(config_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML: {e}")
            

