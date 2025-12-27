import yaml # type:ignore


def load_config(file_path: str) -> dict:
    """
    Load configuration from a Python file.

    Args:
        file_path (str): Path to the configuration file.

    Returns:
        dict: Configuration parameters as a dictionary.
    """
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config 
