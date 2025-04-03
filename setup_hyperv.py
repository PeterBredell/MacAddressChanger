import subprocess
import sys
import ctypes
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_hyperv_status():
    """Check if Hyper-V is already enabled."""
    cmd = 'powershell -Command "Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All"'
    result = subprocess.run(cmd, capture_output=True, text=True)
    return "Enabled" in result.stdout

def enable_hyperv():
    """Enable Hyper-V and required features."""
    features = [
        "Microsoft-Hyper-V-All",
        "Microsoft-Hyper-V",
        "Microsoft-Hyper-V-Tools-All",
        "Microsoft-Hyper-V-Management-PowerShell",
        "Microsoft-Hyper-V-Hypervisor",
        "Microsoft-Hyper-V-Services"
    ]
    
    for feature in features:
        print(f"\nEnabling {feature}...")
        cmd = f'powershell -Command "Enable-WindowsOptionalFeature -Online -FeatureName {feature} -All -NoRestart"'
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error enabling {feature}: {result.stderr}")
            return False
        print(f"{feature} enabled successfully")
    
    return True

def configure_hyperv():
    """Configure Hyper-V settings."""
    commands = [
        # Allow enhanced session mode
        "Set-VMHost -EnableEnhancedSessionMode $true",
        # Set default virtual switch network
        "Set-VMHost -VirtualHardDiskPath $env:SystemDrive\\VM",
        # Enable MAC address spoofing
        "Set-VMNetworkAdapter -VMName * -MacAddressSpoofing On"
    ]

    for cmd in commands:
        print(f"\nExecuting: {cmd}")
        result = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error configuring Hyper-V: {result.stderr}")
            return False
    
    return True

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

    print("Checking Hyper-V status...")
    if check_hyperv_status():
        print("Hyper-V is already enabled.")
    else:
        print("Enabling Hyper-V features...")
        if enable_hyperv():
            print("\nHyper-V features enabled successfully.")
            print("Configuring Hyper-V...")
            if configure_hyperv():
                print("\nHyper-V configured successfully.")
                print("Please restart your computer for changes to take effect.")
            else:
                print("\nError configuring Hyper-V.")
        else:
            print("\nError enabling Hyper-V features.")

    input("\nPress Enter to exit...")
