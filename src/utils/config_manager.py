import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """
    Manages application configuration (loading, saving, defaults).
    """
    DEFAULT_CONFIG = {
        "mode": "Lossy",
        "keep_metadata": False,
        "quality": 85,
        "workers": 4,
        "max_size": "",
        "format": "Keep Original",
        "overwrite": False,
        "output_dir": None,
        "language": "English",
        "check_updates": True,
        "ui_scale": 1.5,
        "theme": "System"
    }

    def __init__(self, filename: str = "config.json"):
        # Currently using local path for portability/simplicity as per existing app behavior
        self.config_path = Path(filename)
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # Update current config with loaded values, preserving defaults for missing keys
                    self.config.update(loaded)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a config value."""
        self.config[key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get entire config dict."""
        return self.config
