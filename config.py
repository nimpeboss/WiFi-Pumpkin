"""Configuration management module"""
import json
from pathlib import Path
from logger import Logger

logger = Logger("config")

class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if self._initialized:
            return
        self.config_file = Path("config.json")
        self.settings = {
            'ap': {
                'ssid': 'Free_Wifi',
                'channel': 6,
                'band': '2.4GHz',
                'gateway_ip': '192.168.1.1',
                'security': 'none'
            },
            'attacks': {
                'dns_spoof': False,
                'arp_poison': False,
                'deauth': False
            },
            'general': {
                'debug': False,
                'require_root': True
            }
        }

        self._initialized = True
        self._load()
    def _load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.settings.update(json.load(f))
                logger.info("Configuration loaded from config.json")
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
                self.save()
        else:
            self.save()

    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            logger.info("Configuration saved to config.json")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")

    def get(self, key, default=None):
        """Get configuration value"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key, value):
        """Set configuration value"""
        keys = key.split('.')
        config = self.settings
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()

    def reset(self):
        """Reset to default configuration"""
        self.settings = {
            'ap': {
                'ssid': 'Free_WiFi',
                'channel': 6,
                'band': '2.4GHz',
                'gateway_ip': '192.168.1.1',
                'security': 'none'
            },
            'attacks': {
                'dns_spoof': False,
                'arp_poison': False,
                'deauth': False
            },
            'general': {
                'debug': False,
                'require_root': True
            }
        }
        self.save()

def get_config():
    """Get config instance"""
    return Config()
