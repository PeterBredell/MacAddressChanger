import subprocess
import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_adapters():
    cmd = 'powershell -Command "Get-NetAdapter | Select-Object Name, MacAddress"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print("\nDebug - Available adapters:")
    print(result.stdout)
    return result.stdout.strip().split("\n")[2:]  # Skip header lines

def change_mac(adapter_name, new_mac):
    # First try to see if we can modify the adapter
    test_cmd = f'powershell -Command "Get-NetAdapter -Name \'{adapter_name}\' | Format-List"'
    result = subprocess.run(test_cmd, capture_output=True, text=True, shell=True)
    print("\nDebug - Adapter details:")
    print(result.stdout)

    # Try to change MAC
    cmd = f'powershell -Command "Set-NetAdapter -Name \'{adapter_name}\' -MacAddress \'{new_mac}\' -Confirm:$false"'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    print("\nDebug - Change MAC result:")
    print(f"stdout: {result.stdout}")
    print(f"stderr: {result.stderr}")
    return result.returncode == 0

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    print("MAC Changer - Debug Mode")
    
    # List adapters
    adapters = get_adapters()
    print("\nSelect adapter:")
    for i, adapter in enumerate(adapters, 1):
        print(f"{i}. {adapter}")

    choice = int(input("\nEnter number: ")) - 1
    adapter_name = adapters[choice].split()[0]  # Get just the adapter name

    # Change MAC
    new_mac = input("Enter new MAC (XX:XX:XX:XX:XX:XX): ").replace(":", "")
    print(f"\nAttempting to change {adapter_name} MAC to {new_mac}")
    
    if change_mac(adapter_name, new_mac):
        print("\nMAC address change attempted.")
    else:
        print("\nFailed to change MAC address.")

