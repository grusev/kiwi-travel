import json
from pathlib import Path
import time


def wait_until(condition_fn, timeout_seconds=5, interval=0.01):
    """
    Wait until condition_fn function returns True or timeout expires.
    """
    start = time.time()
    while time.time() - start < timeout_seconds:
        if condition_fn():
            return True
        time.sleep(interval)
    return False

def load_config(filename):
    """Helper function to load a config file"""
    config_path = Path(__file__).parent.parent / "config" / filename
    with open(config_path, "r") as f:
        return json.load(f)