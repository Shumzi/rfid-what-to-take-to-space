#!/usr/bin/env python3
"""
Configuration loader for RFID Video Player.
Loads RFID to video file mappings from config.json.
"""

import json
import os
from pathlib import Path


CONFIG_FILE = "config.json"


def load_config():
    """Load configuration from config.json."""
    config_path = Path(CONFIG_FILE)
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file {CONFIG_FILE} not found.\n"
            "Please create config.json with rfid_mappings."
        )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Validate config structure
        if "rfid_mappings" not in config:
            raise ValueError("config.json must contain 'rfid_mappings' key")
        
        return config
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error parsing config.json: {e}")
    except IOError as e:
        raise RuntimeError(f"Error reading config.json: {e}")

