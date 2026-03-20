"""Rogue Access Point module"""

import subprocess
import time
from pathlib import Path
from logger import Logger
from utils import NetworkUtils

logger = Logger("access_point")


class RogueAP:
    def __init__(
        self, interface, ssid, channel=6, band="2.4GHz", security="none", password=""
    ):
        self.interface = interface
        self.ssid = ssid
        self.channel = channel
        self.band = band
        self.security = security
        self.password = password
        self.hostapd_process = None
        self.dnsmasq_process = None
        self._running = False
        logger.info(f"RogueAP initialized: SSID={ssid}, Channel={channel}")

    def _generate_hostapd_config(self):
        """Generate hostapd configuration"""
        hw_mode = "a" if self.band == "5GHz" else "g"

        config = f"""interface={self.interface}
driver=nl80211
ssid={self.ssid}
hw_mode={hw_mode}
channel={self.channel}
ieee80211n=1
ignore_broadcast_ssid=0
"""
        if self.security == "wpa2":
            config += f"""wpa=2
wpa_passphrase={self.password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
"""

        return config

    def _generate_dnsmasq_config(self, gateway_ip="192.168.1.1"):
        """Generate dnsmasq configuration"""
        subnet = gateway_ip.rsplit(".", 1)[0]
        config = f"""interface={self.interface}
listen-address={gateway_ip}
dhcp-range={subnet}.100,{subnet}.254,255.255.255.0,3600
dhcp-option=option:router,{gateway_ip}
dhcp-option=option:dns-server,{gateway_ip}
log-queries
"""
        return config

    def start(self, gateway_ip="192.168.1.1"):
        """Start the rogue access point"""
        if self._running:
            logger.warning("AP is already running")
            return
        if not NetworkUtils.requires_root():
            logger.error("Root privileges required")
            return

        try:
            logger.info(f"Configuring interface {self.interface}")
            subprocess.run(
                ["ip", "link", "set", self.interface, "down"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["ip", "addr", "flush", "dev", self.interface],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["ip", "link", "set", self.interface, "up"],
                check=True,
                capture_output=True,
            )
            logger.info(f"Setting IP address {gateway_ip}")
            subprocess.run(
                ["ip", "addr", "add", f"{gateway_ip}/24", "dev", self.interface],
                check=True,
                capture_output=True,
            )

            logger.info("Starting hostapd...")
            hostapd_config = self._generate_hostapd_config()
            config_file = Path("/tmp/hostapd.conf")
            config_file.write_text(hostapd_config)

            self.hostapd_process = subprocess.Popen(
                ["hostapd", str(config_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            time.sleep(2)

            if self.hostapd_process.poll() is not None:
                logger.error("hostapd failed to start")
                return False

            logger.info("Starting dnsmasq...")
            dnsmasq_config = self._generate_dnsmasq_config(gateway_ip)
            dnsmasq_file = Path("/tmp/dnsmasq.conf")
            dnsmasq_file.write_text(dnsmasq_config)

            self.dnsmasq_process = subprocess.Popen(
                ["dnsmasq", "-C", str(config_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            time.sleep(1)

            if self.dnsmasq_process.poll() is not None:
                logger.error("dnsmasq failed to start")
                self.hostapd_process.terminate()
                return False

            NetworkUtils.enable_ip_forwarding()

            self._running = True
            logger.info(f"Rogue AP started: {self.ssid} on channel {self.channel}")
            return True
        except Exception as e:
            logger.error(f"Failed to start AP: {e}")
            self.stop()
            return False

    def stop(self):
        """Stop the rogue access point"""
        if not self._running:
            logger.warning("AP is not running")
            return False
        try:
            if self.hostapd_process:
                logger.info("Stopping hostapd...")
                self.hostapd_process.terminate()
                self.hostapd_process.wait(timeout=5)

            if self.dnsmasq_process:
                logger.info("Stopping dnsmasq...")
                self.dnsmasq_process.terminate()
                self.dnsmasq_process.wait(timeout=5)

            NetworkUtils.disable_ip_forwarding()

            subprocess.run(
                ["ip", "link", "set", self.interface, "down"],
                check=False,
                capture_output=True,
            )
            subprocess.run(
                ["ip", "addr", "flush", "dev", self.interface],
                check=False,
                capture_output=True,
            )

            self._running = False
            logger.info("Rogue AP stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping AP: {e}")
            return False

    def is_running(self):
        """Check if AP is running"""
        return self._running
