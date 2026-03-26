"""WiFi-Pumpkin-NG Main CLI Interface"""
import sys
import argparse
import json
from access_point import RogueAP
from deauth import DeauthAttack
from dns_spoof import DNSSpoofing
from arp_poison import ARPPoisoning
from utils import NetworkUtils
from config import get_config
from logger import Logger

logger = Logger("main")


class WiFiPumpkinCLI:
    """Command-line interface for WiFi-Pumpkin-NG operations."""

    def __init__(self):
        self.config = get_config()
        self.ap = None
        self.deauth = None
        self.dns = None
        self.arp = None

    def check_root(self):
        """Check for root privileges"""
        if not NetworkUtils.requires_root():
            logger.error("This tool requires root privileges")
            return False
        return True

    def handle_ap_start(self, args):
        """Handle AP start command"""
        if not self.check_root():
            return False

        self.ap = RogueAP(
            args.interface,
            args.ssid,
            args.channel,
            args.band,
            args.security,
            args.password,
        )

        if self.ap.start(args.gateway):
            logger.info(f"AP started: {args.ssid}")
            return True
        return False

    def handle_ap_stop(self, args):
        """Handle AP stop command"""
        if self.ap and self.ap.is_running():
            self.ap.stop()
            logger.info("AP stopped")
            return True
        logger.warning("No AP running")
        return False

    def handle_attack_deauth(self, args):
        """Handle deauth attack"""
        if not self.check_root():
            return False

        self.deauth = DeauthAttack(args.interface, args.ap_mac, args.client_mac)

        if self.deauth.start():
            logger.info("Deauth attack started")
            return True
        return False

    def handle_attack_dns(self, args):
        """Handle DNS spoofing"""
        if not self.check_root():
            return False

        self.dns = DNSSpoofing(args.interface)
        self.dns.add_spoof(args.domain, args.spoof_ip)

        if self.dns.start():
            logger.info(f"DNS spoofing started: {args.domain} -> {args.spoof_ip}")
            return True
        return False

    def handle_attack_arp(self, args):
        """Handle ARP poisoning"""
        if not self.check_root():
            return False

        self.arp = ARPPoisoning(args.interface, args.gateway, args.gateway_mac)
        self.arp.add_target(args.target)

        if self.arp.start():
            logger.info(f"ARP poisoning started on {args.target}")
            return True
        return False

    def handle_interfaces(self, args):
        """List wireless interfaces"""
        interfaces = NetworkUtils.list_wireless_interfaces()
        if interfaces:
            logger.info("Available wireless interfaces:")
            for iface in interfaces:
                logger.info(f"  - {iface}")
            return True
        logger.info("No wireless interfaces found")
        return False

    def handle_config_show(self, args):
        """Show configuration"""

        logger.info("Current configuration:")
        print(json.dumps(self.config.settings, indent=2))
        return True

    def handle_config_reset(self, args):
        """Reset configuration"""
        self.config.reset()
        logger.info("Configuration reset to defaults")
        return True

    def run(self, args):
        """Run the CLI"""
        if args.command == "ap":
            if args.ap_command == "start":
                return self.handle_ap_start(args)
            elif args.ap_command == "stop":
                return self.handle_ap_stop(args)

        elif args.command == "attack":
            if args.attack_type == "deauth":
                return self.handle_attack_deauth(args)
            elif args.attack_type == "dns":
                return self.handle_attack_dns(args)
            elif args.attack_type == "arp":
                return self.handle_attack_arp(args)

        elif args.command == "interfaces":
            return self.handle_interfaces(args)

        elif args.command == "config":
            if args.config_action == "show":
                return self.handle_config_show(args)
            elif args.config_action == "reset":
                return self.handle_config_reset(args)

        return False


def create_parser():
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        description="WiFi-Pumpkin-NG - WiFi Penetration Testing Framework"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # AP subcommand
    ap_parser = subparsers.add_parser("ap", help="Access Point commands")
    ap_parser.add_argument("ap_command", choices=["start", "stop"], help="AP action")
    ap_parser.add_argument(
        "-i", "--interface", default="wlan0", help="Wireless interface"
    )
    ap_parser.add_argument("-s", "--ssid", default="Free_WiFi", help="SSID")
    ap_parser.add_argument("-c", "--channel", type=int, default=6, help="Channel")
    ap_parser.add_argument("-b", "--band", choices=["2.4GHz", "5GHz"], default="2.4GHz")
    ap_parser.add_argument("-g", "--gateway", default="192.168.1.1", help="Gateway IP")
    ap_parser.add_argument(
        "--security", choices=["none", "wep", "wpa", "wpa2"], default="none"
    )
    ap_parser.add_argument("--password", default="", help="WiFi password")

    # Attack subcommand
    attack_parser = subparsers.add_parser("attack", help="Attack commands")
    attack_parser.add_argument("attack_type", choices=["deauth", "dns", "arp"])
    attack_parser.add_argument("-i", "--interface", default="wlan0", help="Interface")
    attack_parser.add_argument("-m", "--ap-mac", help="Target AP MAC")
    attack_parser.add_argument("--client-mac", help="Target client MAC")
    attack_parser.add_argument("-d", "--domain", help="Domain to spoof")
    attack_parser.add_argument("--spoof-ip", help="IP to spoof to")
    attack_parser.add_argument("-t", "--target", help="Target IP")
    attack_parser.add_argument("--gateway", default="192.168.1.1", help="Gateway IP")
    attack_parser.add_argument("--gateway-mac", help="Gateway MAC")

    # Interfaces subcommand
    subparsers.add_parser("interfaces", help="List wireless interfaces")

    # Config subcommand
    config_parser = subparsers.add_parser("config", help="Configuration")
    config_parser.add_argument("config_action", choices=["show", "reset"])

    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    cli = WiFiPumpkinCLI()
    success = cli.run(args)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
