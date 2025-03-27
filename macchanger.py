import os
import re
import subprocess
import winreg
import sys
import ctypes
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_network_adapters():
    """Retrieve a list of network adapters with their descriptions."""
    command = 'powershell -Command "Get-NetAdapter | Select-Object Name, InterfaceDescription | ForEach-Object { $_.Name + \'|\' + $_.InterfaceDescription }"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    adapters = result.stdout.strip().split("\n")
    return [tuple(adapter.strip().split("|")) for adapter in adapters if adapter.strip()]

def change_mac_address(adapter_name, adapter_desc, new_mac):
    """Change the MAC address of the specified network adapter."""
    try:
        reg_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as reg:
            with winreg.OpenKey(reg, reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                print(f"\nSearching for adapter in registry: {adapter_desc}")
                
                for i in range(1000):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name, 0, winreg.KEY_READ | winreg.KEY_WRITE) as subkey:
                            try:
                                driver_desc = winreg.QueryValueEx(subkey, "DriverDesc")[0]
                                print(f"Checking adapter: {driver_desc}")
                                
                                if adapter_desc.lower() in driver_desc.lower():
                                    print(f"Found matching adapter: {driver_desc}")
                                    # Try multiple registry values that might control MAC
                                    for mac_key in ["NetworkAddress", "PermanentAddress", "OriginalNetworkAddress"]:
                                        try:
                                            winreg.SetValueEx(subkey, mac_key, 0, winreg.REG_SZ, new_mac)
                                            print(f"Successfully set {mac_key} to {new_mac}")
                                        except WindowsError as we:
                                            print(f"Failed to set {mac_key}: {str(we)}")
                                    return True
                            except WindowsError:
                                continue
                    except WindowsError:
                        break
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def restart_adapter(adapter_name):
    """Restart the network adapter."""
    try:
        print(f"\nDisabling adapter {adapter_name}...")
        disable_cmd = f'powershell -Command "Disable-NetAdapter -Name \'{adapter_name}\' -Confirm:$false"'
        subprocess.run(disable_cmd, shell=True, check=True)
        
        print("Waiting for adapter to fully disable...")
        time.sleep(5)  # Wait 5 seconds
        
        print(f"Enabling adapter {adapter_name}...")
        enable_cmd = f'powershell -Command "Enable-NetAdapter -Name \'{adapter_name}\' -Confirm:$false"'
        subprocess.run(enable_cmd, shell=True, check=True)
        
        print("Waiting for adapter to initialize...")
        time.sleep(5)  # Wait 5 seconds
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error restarting adapter: {str(e)}")
        return False

def get_current_mac(adapter_name):
    """Get the current MAC address of the specified adapter."""
    command = f'powershell -Command "Get-NetAdapter -Name \'{adapter_name}\' | Select-Object -ExpandProperty MacAddress"'
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def validate_mac(mac):
    """Validate the MAC address format."""
    return re.match(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", mac) is not None

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    try:
        print("Welcome to MAC Changer")
        adapters = get_network_adapters()
        if not adapters:
            print("No network adapters found.")
            sys.exit(1)

        print("\nAvailable network adapters:")
        for i, (name, desc) in enumerate(adapters):
            print(f"{i + 1}. {name} ({desc})")

        choice = int(input("\nSelect the adapter to change the MAC address (number): ")) - 1
        if choice < 0 or choice >= len(adapters):
            print("Invalid choice.")
            sys.exit(1)

        adapter_name, adapter_desc = adapters[choice]
        current_mac = get_current_mac(adapter_name)
        print(f"\nCurrent MAC address: {current_mac}")

        new_mac = input("Enter the new MAC address (format: XX:XX:XX:XX:XX:XX): ")
        if not validate_mac(new_mac):
            print("Invalid MAC address format.")
            sys.exit(1)

        new_mac = new_mac.replace(":", "").replace("-", "")
        print("\nChanging MAC address...")
        if change_mac_address(adapter_name, adapter_desc, new_mac):
            print("\nMAC address changed in registry.")
            if restart_adapter(adapter_name):
                print("\nChecking new MAC address...")
                time.sleep(2)  # Give additional time for adapter to stabilize
                new_current_mac = get_current_mac(adapter_name)
                print(f"Previous MAC: {current_mac}")
                print(f"New MAC: {new_current_mac}")
                print(f"Expected MAC: {new_mac.upper()}")
                
                if new_current_mac and new_current_mac.replace("-", "") == new_mac.upper():
                    print("\nMAC address was successfully changed!")
                else:
                    print("\nWarning: MAC address did not change as expected.")
                    print("You may need to:")
                    print("1. Restart your computer")
                    print("2. Check if your network adapter supports MAC address changes")
                    print("3. Verify that you have administrator privileges")
            else:
                print("Failed to restart network adapter.")
        else:
            print("Failed to change MAC address in registry.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

