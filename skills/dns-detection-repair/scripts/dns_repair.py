#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNS Repair Script
Attempts to repair DNS service issues and network connectivity problems.
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
            cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def start_service(service_name: str) -> Dict:
    """Attempt to start a Windows service."""
    result = {
        "service": service_name,
        "success": False,
        "message": ""
    }
    
    # Check current status
    _, _, code = run_command(f'sc query {service_name}')
    
    if code == 0:
        # Try to start the service
        start_output, start_error, start_code = run_command(f'net start {service_name}')
        
        if start_code == 0:
            result["success"] = True
            result["message"] = f"Successfully started {service_name}"
        else:
            # Try alternative method
            sc_start_output, sc_start_error, sc_start_code = run_command(f'sc start {service_name}')
            if sc_start_code == 0:
                result["success"] = True
                result["message"] = f"Successfully started {service_name} via sc"
            else:
                result["message"] = f"Failed to start: {start_error or sc_start_error}"
    else:
        result["message"] = f"Service {service_name} not found"
        
    return result


def set_service_startup(service_name: str, startup_type: str = "auto") -> Dict:
    """Set service startup type."""
    result = {
        "service": service_name,
        "startup_type": startup_type,
        "success": False,
        "message": ""
    }
    
    type_map = {
        "auto": "demand",  # AUTO_START maps to demand in sc config
        "manual": "demand",
        "disabled": "disabled"
    }
    
    output, error, code = run_command(f'sc config {service_name} start= {type_map.get(startup_type, "demand")}')
    
    if code == 0:
        result["success"] = True
        result["message"] = f"Set {service_name} startup type to {startup_type}"
    else:
        result["message"] = f"Failed to set startup type: {error}"
        
    return result


def flush_dns_cache() -> Dict:
    """Flush DNS cache."""
    result = {
        "action": "flush_dns",
        "success": False,
        "message": ""
    }
    
    output, error, code = run_command('ipconfig /flushdns')
    
    if code == 0:
        result["success"] = True
        result["message"] = "DNS cache flushed successfully"
    else:
        result["message"] = f"Failed to flush DNS: {error}"
        
    return result


def renew_ip_config() -> Dict:
    """Renew IP configuration."""
    result = {
        "action": "renew_ip",
        "success": False,
        "message": ""
    }
    
    output, error, code = run_command('ipconfig /renew')
    
    if code == 0:
        result["success"] = True
        result["message"] = "IP configuration renewed successfully"
    else:
        result["message"] = f"Failed to renew IP: {error}"
        
    return result


def register_dns() -> Dict:
    """Register DNS settings."""
    result = {
        "action": "register_dns",
        "success": False,
        "message": ""
    }
    
    output, error, code = run_command('ipconfig /registerdns')
    
    if code == 0:
        result["success"] = True
        result["message"] = "DNS registration successful"
    else:
        result["message"] = f"Failed to register DNS: {error}"
        
    return result


def reset_netsh() -> Dict:
    """Reset Winsock and TCP/IP stack."""
    result = {
        "action": "reset_netsh",
        "success": False,
        "message": ""
    }
    
    # Reset Winsock
    output1, error1, code1 = run_command('netsh winsock reset')
    
    # Reset TCP/IP
    output2, error2, code2 = run_command('netsh int ip reset')
    
    if code1 == 0 and code2 == 0:
        result["success"] = True
        result["message"] = "Winsock and TCP/IP reset successful. Please restart your computer."
    else:
        result["message"] = f"Winsock reset: {'OK' if code1 == 0 else 'FAILED'}, "
        result["message"] += f"TCP/IP reset: {'OK' if code2 == 0 else 'FAILED'}"
        
    return result


def change_dns_servers(primary: str = "114.114.114.114", secondary: str = "8.8.8.8") -> Dict:
    """Change DNS server configuration."""
    result = {
        "action": "change_dns",
        "primary": primary,
        "secondary": secondary,
        "success": False,
        "message": "",
        "interfaces_modified": []
    }
    
    # Get all network interfaces
    output, _, _ = run_command('netsh interface ip show dns')
    lines = output.split('\n')
    
    # Find interface names (simplified approach)
    interfaces = []
    for line in lines:
        if "Ethernet" in line or "Wi-Fi" in line or "以太网" in line or "无线" in line:
            parts = line.split(':')
            if len(parts) > 0:
                iface_name = parts[0].strip()
                interfaces.append(iface_name)
    
    # Also try alternative method
    if not interfaces:
        alt_output, _, _ = run_command('netsh interface show interface')
        for line in alt_output.split('\n')[3:]:  # Skip header lines
            parts = line.split()
            if len(parts) >= 3:
                iface_name = ' '.join(parts[2:])
                if "Connected" in line or "已连接" in line:
                    interfaces.append(iface_name)
    
    success_count = 0
    for iface in interfaces:
        # Set primary DNS
        set_cmd = f'netsh interface ip set dns "{iface}" static {primary}'
        out1, err1, code1 = run_command(set_cmd)
        
        # Set secondary DNS
        add_cmd = f'netsh interface ip add dns "{iface}" {secondary} index=2'
        out2, err2, code2 = run_command(add_cmd)
        
        if code1 == 0:
            success_count += 1
            result["interfaces_modified"].append(iface)
    
    if success_count > 0:
        result["success"] = True
        result["message"] = f"DNS servers changed to {primary} (primary) and {secondary} (secondary)"
    else:
        result["message"] = "Failed to change DNS servers. Please configure manually."
        
    return result


def check_service_status(service_name: str) -> Dict:
    """Check if a service is running."""
    output, _, code = run_command(f'sc query {service_name}')
    
    status_info = {
        "service": service_name,
        "running": False,
        "start_type": "unknown",
        "details": output
    }
    
    if code == 0 and "RUNNING" in output.upper():
        status_info["running"] = True
        
    return status_info


def run_repair_sequence() -> Dict:
    """Run comprehensive DNS repair sequence."""
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "actions": [],
        "services_repaired": [],
        "overall_success": False,
        "restart_required": False,
        "final_status": "unknown"
    }
    
    # Step 1: Start DHCP service
    print("Step 1: Starting DHCP Client service...")
    dhcp_result = start_service("DHCP")
    report["actions"].append({
        "step": 1,
        "action": "start_dhcp",
        **dhcp_result
    })
    if dhcp_result["success"]:
        report["services_repaired"].append("DHCP")
    
    # Step 2: Start DNS Client service
    print("Step 2: Starting DNS Client service...")
    dns_result = start_service("Dnscache")
    report["actions"].append({
        "step": 2,
        "action": "start_dns_client",
        **dns_result
    })
    if dns_result["success"]:
        report["services_repaired"].append("DNS Client")
    
    # Step 3: Flush DNS cache
    print("Step 3: Flushing DNS cache...")
    flush_result = flush_dns_cache()
    report["actions"].append({
        "step": 3,
        **flush_result
    })
    
    # Step 4: Renew IP configuration
    print("Step 4: Renewing IP configuration...")
    renew_result = renew_ip_config()
    report["actions"].append({
        "step": 4,
        **renew_result
    })
    
    # Step 5: Register DNS
    print("Step 5: Registering DNS...")
    register_result = register_dns()
    report["actions"].append({
        "step": 5,
        **register_result
    })
    
    # Step 6: Verify services are running
    print("Step 6: Verifying service status...")
    dhcp_status = check_service_status("DHCP")
    dns_status = check_service_status("Dnscache")
    
    services_ok = dhcp_status["running"] and dns_status["running"]
    
    report["services_status"] = {
        "dhcp": dhcp_status,
        "dns_client": dns_status
    }
    
    if not services_ok:
        # Try setting startup type to auto
        print("Services not running, attempting to set auto-start...")
        set_auto_result = set_service_startup("DHCP", "auto")
        set_dns_result = set_service_startup("Dnscache", "auto")
        
        report["actions"].append({
            "step": 6,
            "action": "set_startup_type",
            "dhcp": set_auto_result,
            "dns": set_dns_result
        })
        
        # Try starting again
        start_dhcp_again = start_service("DHCP")
        start_dns_again = start_service("Dnscache")
        
        report["actions"].append({
            "step": 7,
            "action": "retry_start_services",
            "dhcp": start_dhcp_again,
            "dns": start_dns_again
        })
    
    # Final check
    final_dhcp = check_service_status("DHCP")
    final_dns = check_service_status("Dnscache")
    
    report["final_status"] = {
        "dhcp": final_dhcp,
        "dns": final_dns
    }
    
    report["overall_success"] = final_dhcp["running"] and final_dns["running"]
    
    # Check if restart is needed (for netsh reset)
    if "reset_netsh" in str(report["actions"]):
        report["restart_required"] = True
    
    return report


def print_repair_report(report: Dict):
    """Print formatted repair report."""
    print("=" * 60)
    print("DNS Repair Report")
    print("=" * 60)
    print(f"Time: {report['timestamp']}")
    print(f"Overall Success: {'Yes' if report['overall_success'] else 'No'}")
    print(f"Restart Required: {'Yes' if report['restart_required'] else 'No'}")
    print()
    
    print("Repair Actions:")
    for action in report["actions"]:
        step = action.get("step", "?")
        action_type = action.get("action", "unknown")
        success = action.get("success", False)
        status = "✓" if success else "✗"
        print(f"  {step}. [{status}] {action_type}")
        if action.get("message"):
            print(f"      {action['message']}")
    print()
    
    print("Final Service Status:")
    final = report.get("final_status", {})
    if final:
        dhcp = final.get("dhcp", {})
        dns = final.get("dns", {})
        dhcp_status = "Running" if dhcp.get("running") else "Stopped"
        dns_status = "Running" if dns.get("running") else "Stopped"
        print(f"  - DHCP Client: {dhcp_status}")
        print(f"  - DNS Client: {dns_status}")
    print()
    
    if report["services_repaired"]:
        print(f"Services Repaired: {', '.join(report['services_repaired'])}")
    print()
    
    print("=" * 60)
    
    if report["overall_success"]:
        print("DNS repair completed successfully!")
    else:
        print("Some issues remain. Manual intervention may be required.")
        print("Suggestions:")
        print("  1. Run as Administrator")
        print("  2. Check network adapter drivers")
        print("  3. Consider using alternative DNS servers")


if __name__ == "__main__":
    report = run_repair_sequence()
    print_repair_report(report)
    
    # Also output JSON
    print("\nJSON Output:")
    print(json.dumps(report, indent=2, ensure_ascii=False))
