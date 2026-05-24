#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS Utilities - Shared helper functions for DNS operations.
"""

import subprocess
import socket
import time
from typing import Dict, List, Tuple, Optional


def run_command(cmd: str, timeout: int = 30) -> Tuple[str, str, int]:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def get_system_dns() -> List[str]:
    """Get current system DNS servers."""
    dns_servers = []
    
    # Try to get DNS from ipconfig
    output, _, _ = run_command('ipconfig /all')
    lines = output.split('\n')
    
    for i, line in enumerate(lines):
        if 'DNS Servers' in line or 'DNS 服务器' in line:
            # Next line might contain the actual IP
            if i + 1 < len(lines):
                dns_line = lines[i + 1].strip()
                # Extract IP addresses
                parts = dns_line.split(':')
                if len(parts) > 1:
                    ips = parts[1].strip().split()
                    for ip in ips:
                        if is_valid_ip(ip):
                            dns_servers.append(ip)
    
    return dns_servers


def is_valid_ip(ip: str) -> bool:
    """Check if string is valid IP address."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False


def test_dns_lookup(domain: str, timeout: int = 5) -> Tuple[bool, Optional[str], float]:
    """
    Test DNS lookup for a domain.
    Returns: (success, ip_address, latency_ms)
    """
    try:
        start_time = time.time()
        ip_address = socket.gethostbyname(domain)
        latency = (time.time() - start_time) * 1000
        return True, ip_address, latency
    except socket.gaierror:
        return False, None, 0.0
    except Exception as e:
        return False, None, 0.0


def test_dns_server(server: str, port: int = 53, timeout: int = 5) -> Dict:
    """
    Test connectivity to a DNS server.
    """
    result = {
        "server": server,
        "port": port,
        "reachable": False,
        "latency_ms": None,
        "error": None
    }
    
    try:
        start_time = time.time()
        socket.create_connection((server, port), timeout=timeout)
        latency = (time.time() - start_time) * 1000
        result["reachable"] = True
        result["latency_ms"] = round(latency * 1000, 2)
    except socket.timeout:
        result["error"] = "Connection timed out"
    except ConnectionRefusedError:
        result["error"] = "Connection refused"
    except Exception as e:
        result["error"] = str(e)
    
    return result


def ping_host(host: str, count: int = 2, timeout: int = 3) -> Dict:
    """
    Ping a host to test connectivity.
    """
    result = {
        "host": host,
        "success": False,
        "min_latency": None,
        "avg_latency": None,
        "max_latency": None,
        "packet_loss": None
    }
    
    try:
        cmd = f'ping -n {count} -w {timeout * 1000} {host}'
        output, _, code = run_command(cmd, timeout=30)
        
        if code == 0:
            result["success"] = True
            # Parse ping output for latency (simplified)
            lines = output.split('\n')
            for line in lines:
                if 'Minimum' in line or '最短' in line:
                    try:
                        parts = line.split('=')
                        if len(parts) > 1:
                            latency_part = parts[-1].replace('ms', '').strip()
                            result["min_latency"] = float(latency_part)
                    except:
                        pass
    except Exception as e:
        result["error"] = str(e)
    
    return result


def get_network_interfaces() -> List[Dict]:
    """
    Get list of network interfaces.
    """
    interfaces = []
    
    output, _, _ = run_command('netsh interface show interface')
    lines = output.split('\n')
    
    for line in lines[3:]:  # Skip header lines
        parts = line.split()
        if len(parts) >= 4:
            state = parts[1] if len(parts) > 1 else ""
            iface_type = parts[2] if len(parts) > 2 else ""
            name = ' '.join(parts[3:])
            
            interfaces.append({
                "name": name,
                "state": state,
                "type": iface_type
            })
    
    return interfaces


def get_gateway_ip() -> Optional[str]:
    """
    Get default gateway IP address.
    """
    output, _, _ = run_command('ipconfig | findstr /R "Default Gateway"')
    lines = output.split('\n')
    
    for line in lines:
        if ':' in line:
            parts = line.split(':')
            if len(parts) > 1:
                ip = parts[1].strip()
                if is_valid_ip(ip):
                    return ip
    
    return None


def get_local_ip() -> Optional[str]:
    """
    Get local IP address.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None


def format_bytes(size: int) -> str:
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


class DNSRepairProgress:
    """Progress tracker for DNS repair operations."""
    
    def __init__(self, total_steps: int, description: str):
        self.total_steps = total_steps
        self.current_step = 0
        self.description = description
        self.results = []
    
    def start_step(self, step_num: int, step_name: str):
        self.current_step = step_num
        print(f"[{step_num}/{self.total_steps}] {step_name}...")
    
    def complete_step(self, success: bool, message: str = ""):
        status = "✓" if success else "✗"
        print(f"  [{status}] {message}")
        self.results.append({
            "step": self.current_step,
            "success": success,
            "message": message
        })
    
    def finish(self, overall_success: bool):
        print()
        if overall_success:
            print("✓ All repair steps completed successfully!")
        else:
            print("✗ Some repair steps failed. Check results above.")


# Common DNS servers reference
PUBLIC_DNS_SERVERS = [
    {"name": "114.114.114.114", "provider": "114 DNS", "location": "China"},
    {"name": "114.114.115.115", "provider": "114 DNS", "location": "China"},
    {"name": "8.8.8.8", "provider": "Google DNS", "location": "Global"},
    {"name": "8.8.4.4", "provider": "Google DNS", "location": "Global"},
    {"name": "1.1.1.1", "provider": "Cloudflare DNS", "location": "Global"},
    {"name": "1.0.0.1", "provider": "Cloudflare DNS", "location": "Global"},
    {"name": "208.67.222.222", "provider": "OpenDNS", "location": "Global"},
    {"name": "208.67.220.220", "provider": "OpenDNS", "location": "Global"},
    {"name": "180.76.76.76", "provider": "Baidu DNS", "location": "China"},
    {"name": "223.5.5.5", "provider": "Aliyun DNS", "location": "China"},
    {"name": "223.6.6.6", "provider": "Aliyun DNS", "location": "China"},
]


if __name__ == "__main__":
    # Test utilities
    print("Testing DNS Utilities...")
    print()
    
    print("Local IP:", get_local_ip())
    print("Gateway IP:", get_gateway_ip())
    print("System DNS:", get_system_dns())
    print()
    
    print("Testing DNS server...")
    result = test_dns_server("8.8.8.8")
    print(f"  8.8.8.8: {result}")
    
    print("Testing DNS lookup...")
    success, ip, latency = test_dns_lookup("www.baidu.com")
    print(f"  www.baidu.com: success={success}, ip={ip}, latency={latency}ms")
