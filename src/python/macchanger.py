"""
MAC Address Changer
MIT License
Copyright (c) 2024
See LICENSE file for details.
"""

import wmi
import winreg
import re
import ctypes
import sys
import time
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_adapter_info(adapter_name):
    """Get WMI adapter object and registry info."""
    w = wmi.WMI()
    adapters = w.Win32_NetworkAdapter(Name=adapter_name)
    if not adapters:
        return None
    
    adapter = adapters[0]
    print(f"Debug - PNPDeviceID: {adapter.PNPDeviceID}")
    
    # Use CurrentControlSet instead of ControlSet001
    reg_base = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
    
    # Extract adapter information for different matching methods
    device_id = adapter.PNPDeviceID.split("\\")[-1] if adapter.PNPDeviceID else None
    adapter_guid = None
    
    # Try to find the adapter configuration in the registry using multiple methods
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_base, 0, winreg.KEY_READ) as base_key:
            for i in range(256):
                try:
                    subkey_name = winreg.EnumKey(base_key, i)
                    with winreg.OpenKey(base_key, subkey_name, 0, winreg.KEY_READ) as subkey:
                        # Method 1: Match by DriverDesc (most common)
                        try:
                            driver_desc = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                            if driver_desc == adapter.Name:
                                print(f"Found adapter by DriverDesc: {driver_desc}")
                                return adapter, f"{reg_base}\\{subkey_name}"
                        except WindowsError:
                            pass
                        
                        # Method 2: Match by DeviceInstanceID or PNPDeviceID
                        try:
                            if device_id:
                                device_instance_id = winreg.QueryValueEx(subkey, "DeviceInstanceID")[0]
                                if device_id in device_instance_id:
                                    print(f"Found adapter by DeviceInstanceID: {device_instance_id}")
                                    return adapter, f"{reg_base}\\{subkey_name}"
                        except WindowsError:
                            pass
                        
                        # Method 3: Match by partial name (for cases where names don't match exactly)
                        try:
                            adapter_name_lower = adapter.Name.lower()
                            driver_desc = winreg.QueryValueEx(subkey, "DriverDesc")[0].lower()
                            # Check if significant parts of the name match (not just common words like "adapter")
                            if (adapter_name_lower in driver_desc or 
                                driver_desc in adapter_name_lower or 
                                any(word in driver_desc for word in adapter_name_lower.split() if len(word) > 4)):
                                print(f"Found adapter by partial name match: {driver_desc}")
                                return adapter, f"{reg_base}\\{subkey_name}"
                        except WindowsError:
                            pass
                            
                except WindowsError:
                    break
    except WindowsError as e:
        print(f"Registry error: {e}")
    
    # Try alternative method using NetCfgInstanceId for wireless adapters
    try:
        network_config_path = r"SYSTEM\CurrentControlSet\Control\Network\{4D36E972-E325-11CE-BFC1-08002BE10318}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, network_config_path, 0, winreg.KEY_READ) as network_key:
            for i in range(256):
                try:
                    guid = winreg.EnumKey(network_key, i)
                    connection_path = f"{network_config_path}\\{guid}\\Connection"
                    
                    # Skip virtual adapters and other non-relevant entries
                    if guid == "Descriptions" or len(guid) < 10:
                        continue
                        
                    try:
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, connection_path, 0, winreg.KEY_READ) as conn_key:
                            try:
                                name = winreg.QueryValueEx(conn_key, "Name")[0]
                                if adapter.NetConnectionID == name:
                                    # Found the adapter's GUID, now find the corresponding registry key
                                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_base, 0, winreg.KEY_READ) as class_key:
                                        for j in range(256):
                                            try:
                                                subkey_name = winreg.EnumKey(class_key, j)
                                                with winreg.OpenKey(class_key, subkey_name, 0, winreg.KEY_READ) as subkey:
                                                    try:
                                                        net_cfg_instance_id = winreg.QueryValueEx(subkey, "NetCfgInstanceId")[0]
                                                        if net_cfg_instance_id.lower() == guid.lower():
                                                            print(f"Found adapter by NetCfgInstanceId: {guid}")
                                                            return adapter, f"{reg_base}\\{subkey_name}"
                                                    except WindowsError:
                                                        pass
                                            except WindowsError:
                                                break
                            except WindowsError:
                                pass
                    except WindowsError:
                        pass
                except WindowsError:
                    break
    except WindowsError as e:
        print(f"Network registry error: {e}")
    
    print("Could not find the adapter's registry key. MAC address change may fail.")
    # As a last resort, return the adapter and a best guess for the registry path
    return adapter, None

def verify_mac_with_system_commands(adapter_name, expected_mac):
    """Verify MAC address change using system commands (similar to ipconfig)."""
    try:
        # Run ipconfig /all and capture output
        output = subprocess.check_output("ipconfig /all", shell=True, text=True)
        
        # Find the section for our adapter
        adapter_section = None
        lines = output.splitlines()
        for i, line in enumerate(lines):
            if adapter_name in line:
                adapter_section = lines[i:i+20]  # Grab the next 20 lines which should include the MAC
                break
        
        if not adapter_section:
            return False
        
        # Look for Physical Address (MAC) in this section
        for line in adapter_section:
            if "Physical Address" in line:
                # Extract MAC address (format: XX-XX-XX-XX-XX-XX)
                mac_parts = line.split(":")
                if len(mac_parts) >= 2:
                    current_mac = mac_parts[1].strip().replace("-", "").upper()
                    return current_mac == expected_mac.upper()
        
        return False
    except Exception as e:
        print(f"Error verifying MAC with system commands: {str(e)}, make sure the number starts with 02")
        return False

def configure_virtual_nic():
    """Create and configure a VirtualNIC."""
    try:
        print("Creating a virtual switch...")
        subprocess.run([
            "powershell", "-Command",
            "New-VMSwitch -Name 'VirtualSwitch' -NetAdapterName 'Wi-Fi' -AllowManagementOS $true"
        ], check=True)

        print("Adding a VirtualNIC...")
        subprocess.run([
            "powershell", "-Command",
            "Add-VMNetworkAdapter -ManagementOS -Name 'VirtualNIC' -SwitchName 'VirtualSwitch'"
        ], check=True)

        print("Configuring the VirtualNIC...")
        use_dhcp = input("Do you want to use DHCP for the VirtualNIC? (yes/no): ").strip().lower()
        if use_dhcp == "yes":
            subprocess.run([
                "powershell", "-Command",
                "Set-NetIPInterface -InterfaceAlias 'vEthernet (VirtualNIC)' -Dhcp Enabled"
            ], check=True)
            subprocess.run(["ipconfig", "/renew"], check=True)
        else:
            ip_address = input("Enter the static IP address for the VirtualNIC (e.g., 192.168.1.100): ").strip()
            prefix_length = input("Enter the prefix length (e.g., 24 for 255.255.255.0): ").strip()
            gateway = input("Enter the default gateway (e.g., 192.168.1.1): ").strip()
            subprocess.run([
                "powershell", "-Command",
                f"New-NetIPAddress -InterfaceAlias 'vEthernet (VirtualNIC)' -IPAddress {ip_address} -PrefixLength {prefix_length} -DefaultGateway {gateway}"
            ], check=True)

        print("Routing traffic through the VirtualNIC...")
        subprocess.run([
            "powershell", "-Command",
            "Get-NetRoute | Where-Object { $_.DestinationPrefix -eq '0.0.0.0/0' -and $_.InterfaceAlias -eq 'Wi-Fi' } | Remove-NetRoute"
        ], check=True)
        subprocess.run([
            "powershell", "-Command",
            "New-NetRoute -DestinationPrefix '0.0.0.0/0' -InterfaceAlias 'vEthernet (VirtualNIC)' -NextHop 192.168.1.1"
        ], check=True)

        print("VirtualNIC configured successfully. Traffic is now routed through the VirtualNIC.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error configuring VirtualNIC: {e}")
        return False

def revert_virtual_nic():
    """Revert VirtualNIC changes and restore original configuration."""
    try:
        print("Reverting VirtualNIC changes...")
        subprocess.run([
            "powershell", "-Command",
            "Remove-NetRoute -DestinationPrefix '0.0.0.0/0' -InterfaceAlias 'vEthernet (VirtualNIC)'"
        ], check=True)

        subprocess.run([
            "powershell", "-Command",
            "New-NetRoute -DestinationPrefix '0.0.0.0/0' -InterfaceAlias 'Wi-Fi' -NextHop 192.168.1.1"
        ], check=True)

        subprocess.run([
            "powershell", "-Command",
            "Remove-VMNetworkAdapter -ManagementOS -Name 'VirtualNIC'"
        ], check=True)

        subprocess.run([
            "powershell", "-Command",
            "Remove-VMSwitch -Name 'VirtualSwitch'"
        ], check=True)

        print("VirtualNIC changes reverted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error reverting VirtualNIC changes: {e}")

def change_mac_address(adapter_name, new_mac):
    """Change MAC address using WMI and Registry."""
    if not re.match(r'^[0-9A-F]{12}$', new_mac.upper()):
        print("Invalid MAC address format")
        return False

    info = get_adapter_info(adapter_name)
    if not info:
        print(f"Adapter {adapter_name} not found")
        return False

    adapter, reg_path = info
    print(f"Found adapter: {adapter.Name}")
    print(f"Current MAC: {adapter.MacAddress}")
    
    # Check if this is a wireless adapter
    is_wireless = False
    try:
        # Using WMI to check if this is a wireless adapter
        if hasattr(adapter, 'AdapterType') and adapter.AdapterType:
            is_wireless = 'wireless' in adapter.AdapterType.lower()
        
        # Second method to check if wireless - look for specific names
        if not is_wireless and adapter.Name:
            is_wireless = any(term in adapter.Name.lower() for term in ['wireless', 'wifi', 'wi-fi', '802.11'])
        
        # Get NetConnectionID from the registry if available
        if not is_wireless and hasattr(adapter, 'NetConnectionID') and adapter.NetConnectionID:
            is_wireless = any(term in adapter.NetConnectionID.lower() for term in ['wireless', 'wifi', 'wi-fi'])
    except:
        pass
    
    # If this is a wireless adapter, ensure the MAC has correct format for Windows
    if is_wireless:
        print("Detected wireless adapter - ensuring MAC address format is compatible with Windows.")
        # Check the first octet and modify if needed
        first_byte = int(new_mac[0:2], 16)
        # Windows requires the second bit to be set for wireless adapters
        if first_byte & 0x02 == 0:
            # Set the second bit (locally administered bit)
            first_byte |= 0x02
            new_mac = f"{first_byte:02X}{new_mac[2:]}".upper()
            print(f"Adjusted MAC address to meet Windows wireless requirements: {new_mac}")
    
    if not reg_path:
        print("Warning: Registry path not found. MAC address change may fail.")
        return False
        
    print(f"Registry path: {reg_path}")

    try:
        # Disable adapter
        print("Disabling adapter...")
        adapter.Disable()
        time.sleep(1)

        # Change MAC in registry with full access rights
        print("Updating registry...")
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
                winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.upper())
                print("Registry update successful")
        except WindowsError as e:
            print(f"Registry error: {e}")
            return False

        # Re-enable adapter
        print("Enabling adapter...")
        adapter.Enable()
        time.sleep(5)

        # Verify change using WMI
        wmi_verification = False
        system_verification = False
        
        adapters = wmi.WMI().Win32_NetworkAdapter(Name=adapter_name)
        if adapters and adapters[0].MacAddress and adapters[0].MacAddress.replace(':', '') == new_mac.upper():
            print(f"WMI reports MAC changed to: {adapters[0].MacAddress}")
            wmi_verification = True
        else:
            print("MAC change not reflected in WMI")
        
        # Verify with system commands (ipconfig-like)
        if verify_mac_with_system_commands(adapter_name, new_mac):
            print("System commands confirm MAC address change")
            system_verification = True
        else:
            print("MAC change not reflected in system commands (ipconfig)")
            print("You may need to manually disable and re-enable the adapter from Network Connections")
        
        # Return true only if at least one verification method succeeds
        return wmi_verification or system_verification

    except Exception as e:
        print(f"Error: {str(e)}")
        # Try to re-enable adapter if something went wrong
        try:
            adapter.Enable()
        except:
            pass
        return False

    use_virtual_nic = input("MAC address change failed. Do you want to use a VirtualNIC instead? (yes/no): ").strip().lower()
    if use_virtual_nic == "yes":
        if configure_virtual_nic():
            print("VirtualNIC fallback method succeeded.")
            return True
        else:
            print("VirtualNIC fallback method failed.")
            return False
    else:
        print("MAC address change aborted.")
        return False

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    # List available adapters
    w = wmi.WMI()
    adapters = w.Win32_NetworkAdapter(PhysicalAdapter=True)
    
    print("Available adapters:")
    for i, adapter in enumerate(adapters):
        if adapter.MacAddress:  # Only show adapters with MAC addresses
            print(f"{i + 1}. {adapter.Name} - {adapter.MacAddress}")

    choice = int(input("\nSelect adapter number: ")) - 1
    new_mac = input("Enter new MAC (XXXXXXXXXXXX): ").strip()

    try:
        change_mac_address(adapters[choice].Name, new_mac)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        revert_virtual_nic()

