# WiFi-Pumpkin-NG: Complete Project Documentation

## Project Overview

**WiFi-Pumpkin-NG** is a modern Python 3 rebuild of the original WiFi-Pumpkin penetration testing framework. This project implements a complete WiFi security testing toolkit with the following components:

- **Rogue Access Point (AP)** - Create fake WiFi networks
- **Man-in-the-Middle (MITM) Attacks** - DNS spoofing, ARP poisoning
- **Deauthentication Attacks** - Disconnect clients
- **Traffic Interception & Monitoring** - Capture and analyze packets
- **Plugin System** - Extensible architecture for custom modules

## ⚠️ Legal Disclaimer

**FOR AUTHORIZED SECURITY TESTING ONLY**

This is a penetration testing framework designed for:
- ✅ Authorized security audits
- ✅ Network testing on your own infrastructure
- ✅ Educational purposes
- ✅ Cybersecurity training

**ILLEGAL USES:**
- ❌ Unauthorized network access
- ❌ Attacking networks without permission
- ❌ Intercepting private communications
- ❌ Theft of data or credentials

**You must have explicit written permission to test any network.**

---

## Project Structure

```
wifi-pumpkin-ng/
│
├── README.md                  # Project overview
├── requirements.txt           # Python dependencies
├── main.py                    # CLI entry point
│
├── Core Modules
├── access_point.py            # Rogue AP implementation
├── deauth.py                  # Deauth attack module
├── dns_spoof.py               # DNS spoofing attack
├── arp_poison.py              # ARP poisoning attack
│
├── Configuration & Logging
├── config.py                  # Configuration management
├── logger.py                  # Logging system
├── utils.py                   # Utility functions
│
├── Plugin System
├── plugin_base.py             # Plugin base classes and examples
│
├── Examples
├── example_integrated.py       # Complete integrated example
│
└── logs/                      # Log files directory
    ├── ap.log
    ├── attacks.log
    ├── proxy.log
    └── ...
```

## Component Details

### 1. Access Point (access_point.py)

Creates rogue WiFi networks using hostapd and dnsmasq.

**Features:**
- Multiple SSID support
- Configurable channels (1-13 for 2.4GHz, 36+ for 5GHz)
- Security options (open, WEP, WPA, WPA2)
- DHCP server integration
- Client management
- Status monitoring

**Usage:**
```python
from access_point import RogueAP

ap = RogueAP(
    interface='wlan0',
    ssid='Free_WiFi',
    channel=6,
    band='2.4GHz',
    security='none'
)

ap.start(gateway_ip='192.168.1.1')
# ... do something ...
ap.stop()
```

### 2. Deauthentication Attack (deauth.py)

Disconnects clients from networks using IEEE 802.11 deauth frames.

**Features:**
- Broadcast or targeted deauth
- Configurable frame counts and intervals
- Statistics tracking
- Proper cleanup on stop

**Usage:**
```python
from deauth import DeauthAttack

attack = DeauthAttack(
    interface='wlan0',  # Must be in monitor mode
    ap_mac='AA:BB:CC:DD:EE:FF',
    client_mac='11:22:33:44:55:66'  # Optional
)

attack.start(frame_count=100, interval=0.1)
# ... attack running ...
attack.stop()
```

### 3. DNS Spoofing (dns_spoof.py)

Redirects DNS queries to arbitrary IP addresses.

**Features:**
- Domain-based spoofing
- Wildcard support
- Query interception via Scapy
- Transparent DNS redirection
- Multiple domains per instance

**Usage:**
```python
from dns_spoof import DNSSpoofing

dns = DNSSpoofing(interface='wlan0')
dns.add_spoof('google.com', '192.168.1.1')
dns.add_spoof('facebook.com', '192.168.1.1')
dns.start()
# ... DNS queries redirected ...
dns.stop()
```

### 4. ARP Poisoning (arp_poison.py)

Positions attacker as MITM using ARP spoofing.

**Features:**
- ARP table poisoning
- Multiple target support
- Automatic ARP resolution
- ARP table restoration on cleanup
- Packets sent tracking

**Usage:**
```python
from arp_poison import ARPPoisoning

arp = ARPPoisoning(
    interface='wlan0',
    gateway_ip='192.168.1.1',
    gateway_mac='AA:BB:CC:DD:EE:FF'
)

arp.add_target('192.168.1.100')
arp.add_target('192.168.1.101')
arp.start()
# ... ARP poisoning active ...
arp.stop()  # Automatically restores ARP tables
```

### 5. Configuration System (config.py)

Centralized configuration management with file persistence.

**Features:**
- AP configuration
- MITM proxy settings
- Attack settings
- Logger configuration
- General settings
- JSON-based persistence

**Configuration Structure:**
```json
{
  "ap": {
    "ssid": "Free_WiFi",
    "channel": 6,
    "band": "2.4GHz",
    "security": "none"
  },
  "mitm": {
    "enabled": true,
    "listen_port": 8080
  },
  "attacks": {
    "dns_spoof": false,
    "arp_poison": false,
    "deauth": false
  }
}
```

### 6. Logging System (logger.py)

Comprehensive logging with console and file output.

**Features:**
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- Rotating file handlers
- Timestamp tracking
- Automatic log directory creation
- Separate log files per component

### 7. Utility Functions (utils.py)

Helper functions for network operations.

**Key Classes:**
- `NetworkUtils` - Interface management, IP forwarding, monitor mode
- `MACUtils` - MAC address validation and vendor lookup
- `IPUtils` - IPv4 validation and analysis
- `ProcessUtils` - Process management
- `FileUtils` - File operations

### 8. Plugin System (plugin_base.py)

Extensible plugin architecture for custom modules.

**Base Classes:**
- `PluginBase` - Generic plugin base
- `AttackPlugin` - Custom attack implementations
- `ReconPlugin` - Scanning/discovery modules
- `ProxyPlugin` - HTTP interception and modification

**Example Plugins:**
- `HeaderInjectionPlugin` - Injects custom headers
- `JavaScriptInjectionPlugin` - Injects JavaScript into pages

---

## CLI Usage

### Access Point Commands

```bash
# Start rogue AP
sudo python3 main.py ap start -i wlan0 -s "Free_WiFi" -c 6

# Check AP status
sudo python3 main.py ap status

# Stop AP
sudo python3 main.py ap stop
```

### Attack Commands

```bash
# Deauthentication attack
sudo python3 main.py attack deauth -i wlan0 -m AA:BB:CC:DD:EE:FF

# DNS spoofing
sudo python3 main.py attack dns -i wlan0 -d google.com --spoof 192.168.1.1

# ARP poisoning
sudo python3 main.py attack arp -i wlan0 -t 192.168.1.100 --gateway 192.168.1.1
```

### Other Commands

```bash
# List wireless interfaces
sudo python3 main.py interfaces

# Show configuration
python3 main.py config show

# Reset configuration
python3 main.py config reset
```

---

## Installation & Setup

### Prerequisites

- Linux system (Debian/Ubuntu recommended)
- Python 3.9+
- Root/sudo privileges
- Wireless adapter with monitor mode support

### Required System Packages

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    aircrack-ng \
    hostapd \
    dnsmasq \
    iptables \
    wireless-tools \
    iw \
    net-tools
```

### Install WiFi-Pumpkin-NG

```bash
# Clone or extract the project
cd wifi-pumpkin-ng

# Install Python dependencies
sudo pip3 install -r requirements.txt

# Verify installation
sudo python3 main.py interfaces
```

---

## Usage Examples

### Example 1: Simple Rogue AP

```python
from access_point import RogueAP
import time

ap = RogueAP(
    interface='wlan0',
    ssid='Guest_Network',
    channel=11,
    band='2.4GHz'
)

if ap.start():
    print("AP running. Press Ctrl+C to stop...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ap.stop()
```

### Example 2: Deauth Attack

```python
from deauth import DeauthAttack
import time

# Target AP: AA:BB:CC:DD:EE:FF
attack = DeauthAttack(
    interface='wlan0',
    ap_mac='AA:BB:CC:DD:EE:FF'
)

if attack.start(frame_count=100, interval=0.5):
    print("Deauth attack running...")
    time.sleep(10)
    attack.stop()
    print(f"Stats: {attack.get_stats()}")
```

### Example 3: MITM Setup (AP + DNS + ARP)

```python
from access_point import RogueAP
from dns_spoof import DNSSpoofing
from arp_poison import ARPPoisoning
import time

# Start AP
ap = RogueAP('wlan0', 'FreeWiFi', 6)
ap.start('192.168.1.1')

# Start DNS spoofing
dns = DNSSpoofing('wlan0')
dns.add_spoof('example.com', '192.168.1.1')
dns.start()

# Start ARP poisoning
arp = ARPPoisoning('wlan0', '192.168.1.1', 'AA:BB:CC:DD:EE:FF')
arp.add_target('192.168.1.100')
arp.start()

print("MITM setup complete. Running for 30 seconds...")
time.sleep(30)

# Cleanup
dns.stop()
arp.stop()
ap.stop()
```

### Example 4: Complete Integration

See `example_integrated.py` for a comprehensive example showing all features.

---

## Creating Custom Plugins

### Attack Plugin Example

```python
from plugin_base import AttackPlugin

class CustomRangeAttack(AttackPlugin):
    metadata = {
        'name': 'Custom Range Attack',
        'version': '1.0.0',
        'description': 'Attack multiple targets in IP range',
        'author': 'Security Team',
        'attack_type': 'custom'
    }
    
    def on_load(self):
        self.logger.info("Custom attack loaded")
        return True
    
    def on_unload(self):
        return True
    
    def start(self):
        self._running = True
        self.logger.info("Starting range attack...")
        return True
    
    def stop(self):
        self._running = False
        return True
    
    def execute(self, ip_range):
        # Implement custom attack logic
        pass
    
    def get_stats(self):
        return {'running': self._running}
```

### Proxy Interceptor Plugin Example

```python
from plugin_base import ProxyPlugin

class CredentialLogger(ProxyPlugin):
    metadata = {
        'name': 'Credential Logger',
        'version': '1.0.0',
        'description': 'Logs credentials from HTTP requests',
        'author': 'Security Team',
        'proxy_type': 'http_modifier'
    }
    
    def on_load(self):
        return True
    
    def on_unload(self):
        return True
    
    def on_http_request(self, request):
        # Log request bodies that might contain credentials
        if hasattr(request, 'body'):
            self.logger.debug(f"Request: {request.body}")
        return request
    
    def execute(self):
        return {"logging": True}
```

---

## Architecture & Design Patterns

### 1. Singleton Pattern
- Configuration, LoggerManager, PluginManager use singleton pattern
- Ensures single instance across application

### 2. Manager Pattern
- APManager, DeauthAttackManager, etc.
- Manages lifecycle of multiple instances

### 3. Thread-Safe Operations
- Threading locks for concurrent access
- Daemon threads for background operations

### 4. Plugin Architecture
- Base classes define interfaces
- Plugins implement specific functionality
- Dynamic loading/unloading capability

---

## Network Requirements

### Monitor Mode Interface
Most attacks require wireless interface in monitor mode:

```bash
# Enable monitor mode
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ip link set wlan0 up

# Verify
iwconfig wlan0

# Disable monitor mode
sudo ip link set wlan0 down
sudo iwconfig wlan0 mode managed
sudo ip link set wlan0 up
```

### IP Forwarding
MITM attacks require IP forwarding:

```bash
# Enable
sudo sysctl -w net.ipv4.ip_forward=1

# Disable
sudo sysctl -w net.ipv4.ip_forward=0
```

---

## Troubleshooting

### hostapd won't start
- Check interface compatibility
- Verify wireless adapter supports AP mode
- Check regulatory domain settings

### DNS spoofing not working
- Ensure interface is correct
- Verify dnsmasq is running
- Check firewall rules

### Deauth attack ineffective
- Interface must be in monitor mode
- MAC addresses must be correct
- Increase frame count or reduce interval

### ARP restore not working
- Obtain correct gateway MAC address
- Ensure gateway is reachable
- May need manual ARP table correction

---

## Performance Considerations

1. **Thread Management** - Use daemon threads to prevent hanging
2. **Memory** - Log rotation prevents unbounded growth
3. **Network** - Consider bandwidth impact of high-frequency attacks
4. **CPU** - Scapy operations can be CPU-intensive at scale

---

## Security Best Practices

1. **Run in isolated network** - Never test on production networks
2. **Log everything** - Maintain audit trails
3. **Use strong authentication** - If using AP security
4. **Monitor resource usage** - Prevent DoS conditions
5. **Clean up properly** - Restore network state on exit

---

## Contributing & Extending

To contribute:

1. Fork the project
2. Create feature branch
3. Implement changes with tests
4. Follow PEP 8 style guidelines
5. Submit pull request with documentation

To extend with custom modules:

1. Create new module in root or `plugins/` directory
2. Follow existing patterns and structure
3. Add logging using `get_logger()`
4. Document thoroughly
5. Test on multiple systems

---

## References

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [IEEE 802.11 Deauthentication](https://en.wikipedia.org/wiki/Wi-Fi_deauthentication_attack)
- [ARP Spoofing](https://en.wikipedia.org/wiki/ARP_spoofing)
- [DNS Spoofing](https://en.wikipedia.org/wiki/DNS_spoofing)
- [Original WiFi-Pumpkin](https://github.com/P0cL4bs/WiFi-Pumpkin)

---

## License

MIT License - See LICENSE file for details

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions  
- Security: Report to maintainers privately

---

## Disclaimer

Use responsibly. Unauthorized network access is illegal. Always obtain proper authorization before testing.

**Authors are not responsible for misuse of this software.**
