# WiFi-Pumpkin-NG: A Modern WiFi Penetration Testing Framework

A complete rebuild of the WiFi-Pumpkin framework in Python 3 with improved architecture, modularity, and learning value. This tool is designed for authorized security testing and educational purposes only.

## ⚠️ Legal Disclaimer

**This tool is for authorized penetration testing and educational purposes ONLY.** Unauthorized access to computer networks is illegal. Only use this framework on networks you own or have explicit written permission to test.

## Features

- **Rogue Access Point (AP)** - Create fake WiFi networks
- **Man-in-the-Middle (MITM) Proxy** - Intercept and modify HTTP/HTTPS traffic
- **DNS Spoofing** - Redirect DNS queries to custom IPs
- **ARP Poisoning** - Perform ARP spoofing attacks
- **Deauth Attacks** - Disconnect clients from access points
- **Credential Monitoring** - Capture authentication attempts
- **Plugin System** - Extensible architecture for custom modules
- **Traffic Analysis** - Monitor and log network traffic
- **Session Hijacking** - Cookie/session token capture
- **Web Dashboard** - Modern CLI interface for management

## Architecture

```
wifi-pumpkin-ng/
├── core/                    # Core functionality
│   ├── access_point.py     # Rogue AP management
│   ├── mitm_proxy.py       # MITM proxy engine
│   ├── sniffer.py          # Packet sniffing
│   └── utils.py            # Helper utilities
├── attacks/                 # Attack modules
│   ├── deauth.py           # Deauth attacks
│   ├── dns_spoof.py        # DNS spoofing
│   ├── arp_poison.py       # ARP poisoning
│   └── credential_capture.py
├── plugins/                 # Extensible plugins
│   ├── plugin_base.py      # Plugin interface
│   └── examples/           # Example plugins
├── config/                 # Configuration management
├── logger/                 # Logging utilities
└── main.py                # Entry point
```

## Requirements

- Python 3.9+
- Linux (Debian/Ubuntu recommended)
- Root/sudo privileges
- Compatible wireless adapter with monitor mode support

## Installation

```bash
git clone https://github.com/yourusername/wifi-pumpkin-ng.git
cd wifi-pumpkin-ng
sudo pip3 install -r requirements.txt
sudo python3 main.py
```

## Quick Start

### 1. Start the Rogue AP

```python
from core.access_point import RogueAP

ap = RogueAP(
    interface='wlan0',
    ssid='Free_WiFi',
    channel=6,
    band='2.4GHz'
)
ap.start()
```

### 2. Enable MITM Proxy

```python
from core.mitm_proxy import MITMProxy

proxy = MITMProxy(
    listen_port=8080,
    upstream_proxy=None
)
proxy.start()
```

### 3. Perform DNS Spoofing

```python
from attacks.dns_spoof import DNSSpoofing

dns = DNSSpoofing(
    interface='wlan0',
    target_domain='google.com',
    spoof_ip='192.168.1.100'
)
dns.start()
```

## Core Modules

### Access Point (access_point.py)
- Create rogue WiFi networks
- Handle DHCP server
- Manage client connections
- Control bandwidth

### MITM Proxy (mitm_proxy.py)
- Transparent HTTP/HTTPS interception
- Request/response modification
- Plugin-based traffic injection
- Session logging

### Sniffer (sniffer.py)
- Packet capture and analysis
- Protocol filtering (HTTP, DNS, ARP, etc.)
- Credential extraction
- Traffic statistics

### Attacks Module
- **Deauth**: Disconnect clients from networks
- **DNS Spoofing**: Redirect domain queries
- **ARP Poisoning**: Position as MITM on network
- **Credential Capture**: Extract auth attempts

## Plugin Development

Create custom plugins by extending `PluginBase`:

```python
from plugins.plugin_base import PluginBase

class MyPlugin(PluginBase):
    metadata = {
        'name': 'My Custom Plugin',
        'version': '1.0',
        'description': 'Does something cool',
        'author': 'Your Name'
    }
    
    def on_http_request(self, request):
        """Called on every HTTP request"""
        print(f"Request: {request.url}")
        return request
    
    def on_http_response(self, response):
        """Called on every HTTP response"""
        return response
```

## Configuration

Configuration managed via `config/settings.json`:

```json
{
  "interface": "wlan0",
  "ap": {
    "ssid": "Free_WiFi",
    "channel": 6,
    "band": "2.4GHz",
    "security": "none"
  },
  "mitm": {
    "enabled": true,
    "intercept_https": false,
    "port": 8080
  },
  "attacks": {
    "dns_spoof": false,
    "arp_poison": false,
    "deauth": false
  }
}
```

## Usage Examples

See `examples/` directory for complete working examples:

- `basic_ap.py` - Simple rogue AP
- `mitm_intercept.py` - HTTP interception
- `dns_redirect.py` - DNS spoofing
- `credential_stealer.py` - Capture credentials
- `combined_attack.py` - Full integration example

## Logging

All activities logged to `logs/` directory:

```
logs/
├── ap.log          # Access point events
├── proxy.log       # Proxy traffic
├── sniffer.log     # Captured packets
├── attacks.log     # Attack activities
└── credentials.log # Captured credentials
```

## Contributing

Contributions are welcome! Please:

1. Follow PEP 8 style guidelines
2. Add unit tests for new features
3. Update documentation
4. Test on Debian/Ubuntu

## Disclaimer

This software is provided for educational and authorized security testing purposes. Unauthorized access to computer networks is illegal. The authors are not responsible for misuse.

## References

- Original WiFi-Pumpkin: https://github.com/P0cL4bs/WiFi-Pumpkin
- Scapy: https://scapy.readthedocs.io/
- Hostapd: https://w1.fi/hostapd/
- Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html

## License

MIT License - See LICENSE file

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Community: Security research forums
