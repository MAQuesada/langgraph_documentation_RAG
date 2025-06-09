import yaml
import os
import re
from dotenv import load_dotenv
from pathlib import Path

def load_config(config_path: str = None) -> dict:
    """
    Load configuration from a YAML file and expand environment variables.
    
    Args:
        config_path (str, optional): Path to config file. Defaults to "config.yaml" in the same directory as this script.
    
    Returns:
        dict: Parsed configuration with environment variables expanded.
    
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If YAML parsing fails
    """
    # Load environment variables first
    load_dotenv()
    
    # Set default config path if not provided
    if config_path is None:
        config_path = Path(__file__).resolve().parent / "config.yaml"
    else:
        config_path = Path(config_path)
    
    # Check file exists
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    # Load and parse YAML
    try:
        with open(config_path, 'r') as f:
            raw_config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parsing error: {e}") from e
    
    # Expand environment variables
    def _expand_env_vars(obj):
        if isinstance(obj, dict):
            return {k: _expand_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_expand_env_vars(v) for v in obj]
        elif isinstance(obj, str):
            return re.sub(
                r'\$\{(.+?)\}',  # Matches ${VAR_NAME}
                lambda m: os.getenv(m.group(1), m.group(0)),  # Default to original if not found
                obj
            )
        return obj
    
    return _expand_env_vars(raw_config)
