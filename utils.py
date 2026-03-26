"""Utility functions for WiFi-Pumpkin-NG"""

import subprocess
import os
import re
from logger import Logger

logger = Logger(__name__)


class NetworkUtils:
    """Utility methods for network-related operations."""

    @staticmethod
    def requires_root():
        """Check if running as root"""
        return os.geteuid() == 0

    @staticmethod
    def enable_ip_forwarding():
        """Enable IP forwarding"""
        try:
            subprocess.run(
                ["sysctl", "-w", "net.ipv4.ip_forward=1"],
                check=True,
                capture_output=True,
            )
            logger.info("IP forwarding enabled")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to enable IP forwarding: {e}")
            return False

    @staticmethod
    def disable_ip_forwarding():
        """Disable IP forwarding"""
        try:
            subprocess.run(
                ["sysctl", "-w", "net.ipv4.ip_forward=0"],
                check=True,
                capture_output=True,
            )
            logger.info("IP forwarding disabled")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to disable IP forwarding: {e}")
            return False

    @staticmethod
    def get_interface_mac(interface):
        """Get MAC address of interface"""
        try:
            result = subprocess.run(
                ["cat", f"/sys/class/net/{interface}/address"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to get interface MAC for {interface}: {e}")
            return None

    @staticmethod
    def list_wireless_interfaces():
        """List wireless interfaces"""
        try:
            result = subprocess.run(
                ["iwconfig"], capture_output=True, text=True, check=True
            )

            interfaces = re.findall(r"^(\w+)\s+IEEE", result.stdout, re.MULTILINE)
            return interfaces
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logger.error(f"Failed to list wireless interfaces: {e}")
            return []

    @staticmethod
    def enable_monitor_mode(interface):
        """Enable monitor mode"""
        try:
            subprocess.run(
                ["ip", "link", "set", interface, "down"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["iwconfig", interface, "mode", "monitor"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["ip", "link", "set", interface, "up"], check=True, capture_output=True
            )
            logger.info(f"Monitor mode enabled on {interface}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to enable monitor mode: {e}")
            return False

    @staticmethod
    def disable_monitor_mode(interface):
        """Disable monitor mode"""
        try:
            subprocess.run(
                ["ip", "link", "set", interface, "down"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["iwconfig", interface, "mode", "managed"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["ip", "link", "set", interface, "up"], check=True, capture_output=True
            )
            logger.info(f"Monitor mode disabled on {interface}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to disable monitor mode: {e}")
            return False

    @staticmethod
    def set_channel(interface, channel):
        """Set wireless channel"""
        try:
            subprocess.run(
                ["iwconfig", interface, "channel", str(channel)],
                check=True,
                capture_output=True,
            )
            logger.info(f"Channel {channel} set on {interface}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to set channel: {e}")
            return False
