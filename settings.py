from pathlib import Path

import yaml


BASE_DIR = Path(__file__).parent
config_path = BASE_DIR / 'config' / 'config.yaml'


def get_yaml(path: Path) -> dict:
    with open(path) as f:
        parsed_config = yaml.safe_load(f)
        return parsed_config


config = get_yaml(config_path)
