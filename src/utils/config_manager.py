import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

class ConfigManager:
    """
    Manages application configuration (loading, saving, defaults).
    @spec: FR-021 - Configuration storage following OS standards
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
        "ui_scale": 0,  # 0 means auto-detect
        "theme": "System"
    }

    def __init__(self, filename: str = "config.json"):
        # @spec: FR-021 - Store config in OS-standard locations
        self.config_dir = self._get_config_dir()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.config_dir / filename
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()
    
    def _get_config_dir(self) -> Path:
        """Get platform-specific config directory following OS standards."""
        system = sys.platform
        
        if system == "win32":
            # Windows: %APPDATA%\TerryOptImg\
            appdata = os.environ.get("APPDATA", "")
            if appdata:
                return Path(appdata) / "TerryOptImg"
            # Fallback
            return Path.home() / "AppData" / "Roaming" / "TerryOptImg"
            
        elif system == "darwin":
            # macOS: ~/Library/Application Support/TerryOptImg/
            return Path.home() / "Library" / "Application Support" / "TerryOptImg"
            
        else:
            # Linux and other Unix-like: ~/.config/terryoptimg/
            # Respect XDG_CONFIG_HOME if set
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config:
                return Path(xdg_config) / "terryoptimg"
            # Default to ~/.config/terryoptimg
            return Path.home() / ".config" / "terryoptimg"

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
