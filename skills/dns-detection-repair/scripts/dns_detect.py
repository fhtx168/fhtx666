#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS Detection Script
Detects DNS service status, resolution issues, and network connectivity.
"""

import subprocess
import socket
import time
import json
from typing import Dict, List, Tuple, Optional


def run_command(cmd: str) -> Tuple[str, str, int]:
    """Execute shell command and return output."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def check_dhcp_service() -> Dict:
    """Check DHCP Client service status."""
    output, _, code = run_command('sc query DHCP')
    
    service_info = {
        "service": "DHCP Client",
        "running": False,
        "start_type": "unknown",
        "details": ""
    }
    
    if code == 0 and "RUNNING" in output.upper():
        service_info["running"] = True
        service_info["details"] = "DHCP service is running normally"
        
    # Get service startup type
    type_output, _, _ = run_command('sc qc DHCP')
    if "AUTO_START" in type_output.upper():
        service_info["start_type"] = "auto"
    elif "DEMAND_START" in type_output.upper():
        service_info["start_type"] = "manual"
        
    return service_info


def check_dns_service() -> Dict:
    """Check DNS Client service status."""
    output, _, code = run_command('sc query Dnscache')
    
    service_info = {
        "service": "DNS Client",
        "running": False,
        "start_type": "unknown",
        "details": ""
    }
    
    if code == 0 and "RUNNING" in output.upper():
        service_info["running"] = True
        service_info["details"] = "DNS service is running normally"
        
    # Get service startup type
    type_output, _, _ = run_command('sc qc Dnscache')
    if "AUTO_START" in type_output.upper():
        service_info["start_type"] = "auto"
    elif "DEMAND_START" in type_output.upper():
        service_info["start_type"] = "manual"
        
    return service_info


def test_dns_resolution(domain: str = "www.baidu.com") -> Dict:
    """Test DNS resolution for a given domain."""
    result = {
        "domain": domain,
        "success": False,
        "ip_address": None,
        "latency_ms": None,
        "error": None
    }
    
    try:
        start_time = time.time()
        ip_address = socket.gethostbyname(domain)
        latency = (time.time() - start_time) * 1000
        
        result["success"] = True
        result["ip_address"] = ip_address
        result["latency_ms"] = round(latency, 2)
    except socket.gaierror as e:
        result["error"] = f"DNS resolution failed: {str(e)}"
    except Exception as e:
        result["error"] = f"Error: {str(e)}"
        
    return result


def test_dns_servers() -> List[Dict]:
    """Test common DNS servers."""
    dns_servers = [
        {"name": "114.114.114.114", "provider": "114 DNS"},
        {"name": "8.8.8.8", "provider": "Google DNS"},
        {"name": "1.1.1.1", "provider": "Cloudflare DNS"},
    ]
    
    results = []
    for server in dns_servers:
        result = {
            "server": server["name"],
            "provider": server["provider"],
            "reachable": False,
            "latency_ms": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            socket.create_connection((server["name"], 53), timeout=5)
            latency = (time.time() - start_time) * 1000
            
            result["reachable"] = True
            result["latency_ms"] = round(latency * 1000, 2)  # Convert to ms
        except Exception as e:
            result["error"] = str(e)
            
        results.append(result)
        
    return results


def get_dns_cache_info() -> Dict:
    """Get DNS cache information."""
    output, _, code = run_command('ipconfig /displaydns')
    
    cache_info = {
        "entries": 0,
        "content": []
    }
    
    if code == 0:
        lines = output.split('\n')
        # Count records (simplified)
        cache_info["entries"] = len([l for l in lines if 'Record Name' in l])
        cache_info["content"] = lines[:20]  # First 20 lines for preview
        
    return cache_info


def check_network_connectivity() -> Dict:
    """Check basic network connectivity."""
    connectivity = {
        "gateway": {"reachable": False, "ip": None},
        "dns_server": {"reachable": False, "ip": None},
        "internet": {"reachable": False}
    }
    
    # Get gateway IP
    output, _, _ = run_command('ipconfig | findstr /R "Default Gateway"')
    lines = output.split('\n')
    if lines and lines[0]:
        parts = lines[0].split(':')
        if len(parts) > 1:
            gateway_ip = parts[1].strip()
            connectivity["gateway"]["ip"] = gateway_ip
            
            # Test gateway
            try:
                socket.create_connection((gateway_ip, 80), timeout=3)
                connectivity["gateway"]["reachable"] = True
            except:
                pass
    
    # Test internet connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        connectivity["internet"]["reachable"] = True
    except:
        pass
        
    return connectivity


def run_full_dns_detection() -> Dict:
    """Run comprehensive DNS detection."""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "services": {},
        "dns_resolution": {},
        "dns_servers": [],
        "network_connectivity": {},
        "overall_status": "unknown",
        "issues": [],
        "recommendations": []
    }
    
    # Check services
    report["services"]["dhcp"] = check_dhcp_service()
    report["services"]["dns_client"] = check_dns_service()
    
    # Check if services are running
    services_ok = report["services"]["dhcp"]["running"] and report["services"]["dns_client"]["running"]
    
    # Test DNS resolution
    report["dns_resolution"] = test_dns_resolution()
    
    # Test DNS servers
    report["dns_servers"] = test_dns_servers()
    
    # Check network connectivity
    report["network_connectivity"] = check_network_connectivity()
    
    # Determine overall status and issues
    issues = []
    recommendations = []
    
    if not report["services"]["dhcp"]["running"]:
        issues.append("DHCP service is not running")
        recommendations.append("Start DHCP Client service")
        
    if not report["services"]["dns_client"]["running"]:
        issues.append("DNS Client service is not running")
        recommendations.append("Start DNS Client service")
        
    if not report["dns_resolution"]["success"]:
        issues.append(f"DNS resolution failed for {report['dns_resolution']['domain']}")
        recommendations.append("Check DNS server configuration")
        
    if report["dns_resolution"]["latency_ms"] and report["dns_resolution"]["latency_ms"] > 500:
        issues.append(f"High DNS latency: {report['dns_resolution']['latency_ms']}ms")
        recommendations.append("Consider using faster DNS servers")
        
    # Check if any DNS server is reachable
    dns_reachable = any(s["reachable"] for s in report["dns_servers"])
    if not dns_reachable:
        issues.append("All DNS servers are unreachable")
        recommendations.append("Check network connection")
        
    report["issues"] = issues
    report["recommendations"] = recommendations
    
    if not issues:
        report["overall_status"] = "healthy"
    elif len(issues) <= 2:
        report["overall_status"] = "warning"
    else:
        report["overall_status"] = "critical"
        
    return report


def print_report(report: Dict):
    """Print formatted detection report."""
    print("=" * 60)
    print("DNS Detection Report")
    print("=" * 60)
    print(f"Time: {report['timestamp']}")
    print(f"Overall Status: {report['overall_status'].upper()}")
    print()
    
    print("Services Status:")
    for service_name, service_info in report["services"].items():
        status = "ok Running" if service_info["running"] else "fail Stopped"
        print(f"  - {service_info['service']}: {status}")
    print()
    
    print("DNS Resolution Test:")
    if report["dns_resolution"]["success"]:
        print(f"  - Domain: {report['dns_resolution']['domain']}")
        print(f"  - IP: {report['dns_resolution']['ip_address']}")
        print(f"  - Latency: {report['dns_resolution']['latency_ms']}ms")
    else:
        print(f"  - Failed: {report['dns_resolution']['error']}")
    print()
    
    print("DNS Server Reachability:")
    for server in report["dns_servers"]:
        status = "ok" if server["reachable"] else "fail"
        latency_info = f" ({server['latency_ms']}ms)" if server["latency_ms"] else ""
        print(f"  - {status} {server['provider']} ({server['server']}){latency_info}")
    print()
    
    if report["issues"]:
        print("Issues Found:")
        for issue in report["issues"]:
            print(f"  - {issue}")
        print()
        
    if report["recommendations"]:
        print("Recommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    report = run_full_dns_detection()
    print_report(report)
    
    # Also output JSON for programmatic use
    print("\nJSON Output:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
