import subprocess
import sys
import os

def install_latex():
    """Install MiKTeX for LaTeX support."""
    print("Installing MiKTeX (LaTeX) for text rendering...")
    
    # Download MiKTeX installer
    download_cmd = [
        "powershell",
        "-Command",
        "(New-Object System.Net.WebClient).DownloadFile('https://miktex.org/download/win/basic-miktex-x64.exe', 'basic-miktex-x64.exe')"
    ]
    
    print("Downloading MiKTeX installer...")
    subprocess.run(download_cmd, check=True)
    
    # Install MiKTeX silently
    install_cmd = [
        "basic-miktex-x64.exe",
        "--unattended",
        "--shared",
        "--auto-install=yes"
    ]
    
    print("Installing MiKTeX (this may take a while)...")
    subprocess.run(install_cmd, check=True)
    
    # Clean up installer
    os.remove("basic-miktex-x64.exe")
    print("MiKTeX installation completed!")

def main():
    try:
        install_latex()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
