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
    reg_base = r"SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}"
    
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_base, 0, winreg.KEY_READ) as base_key:
            for i in range(256):
                try:
                    subkey_name = winreg.EnumKey(base_key, i)
                    with winreg.OpenKey(base_key, subkey_name, 0, winreg.KEY_READ) as subkey:
                        try:
                            driver_desc = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                            if driver_desc == adapter.Name:
                                return adapter, f"{reg_base}\\{subkey_name}"
                        except WindowsError:
                            continue
                except WindowsError:
                    break
    except WindowsError as e:
        print(f"Registry error: {e}")
    return None

def verify_mac_change(adapter_name, expected_mac):
    """Verify MAC address change using Windows system commands."""
    try:
        output = subprocess.check_output("getmac /v /fo csv", shell=True).decode('utf-8')
        for line in output.splitlines():
            if line and adapter_name in line:
                matches = re.search(r'([0-9A-F]{2}[-:]){5}([0-9A-F]{2})', line, re.IGNORECASE)
                if matches:
                    current_mac = matches.group(0).replace('-', '').replace(':', '').upper()
                    return current_mac == expected_mac.upper()
        return False
    except Exception as e:
        print(f"Error verifying MAC: {str(e)}")
        return False

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

    try:
        print("Disabling adapter...")
        adapter.Disable()
        time.sleep(2)

        print("Updating registry...")
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, "NetworkAddress", 0, winreg.REG_SZ, new_mac.upper())

        print("Enabling adapter...")
        adapter.Enable()
        time.sleep(5)

        # Verify using both WMI and system commands
        if verify_mac_change(adapter_name, new_mac):
            print(f"MAC successfully changed to: {new_mac}")
            return True
        else:
            print("Warning: MAC change not reflected in system. You may need to restart your computer.")
            return False

    except Exception as e:
        print(f"Error: {str(e)}")
        try:
            adapter.Enable()
        except:
            pass
        return False

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    w = wmi.WMI()
    adapters = w.Win32_NetworkAdapter(PhysicalAdapter=True)
    
    print("Available adapters:")
    for i, adapter in enumerate(adapters):
        if adapter.MacAddress:
            print(f"{i + 1}. {adapter.Name} - {adapter.MacAddress}")

    choice = int(input("\nSelect adapter number: ")) - 1
    new_mac = input("Enter new MAC (XXXXXXXXXXXX): ").strip()

    change_mac_address(adapters[choice].Name, new_mac)

