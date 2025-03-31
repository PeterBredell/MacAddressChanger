import wmi
import winreg
import re
import ctypes
import sys
import time

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
    
    # Try to find adapter in registry
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
    print(f"Registry path: {reg_path}")

    try:
        # Disable adapter
        print("Disabling adapter...")
        adapter.Disable()
        time.sleep(2)

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

        # Verify change
        adapters = wmi.WMI().Win32_NetworkAdapter(Name=adapter_name)
        if adapters and adapters[0].MacAddress and adapters[0].MacAddress.replace(':', '') == new_mac.upper():
            print(f"MAC successfully changed to: {adapters[0].MacAddress}")
            return True
        else:
            print("MAC change failed or not yet reflected")
            return False

    except Exception as e:
        print(f"Error: {str(e)}")
        # Try to re-enable adapter if something went wrong
        try:
            adapter.Enable()
        except:
            pass
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

    change_mac_address(adapters[choice].Name, new_mac)

