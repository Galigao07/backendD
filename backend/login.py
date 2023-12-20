import platform
import subprocess

def get_serial_number():
    try:
        system = platform.system()
        if system == 'Windows':
            # Retrieve serial number using WMIC (Windows Management Instrumentation Command-line)
            wmic_output = subprocess.check_output('wmic bios get serialnumber').decode().strip()
            lines = wmic_output.split('\n')
            if len(lines) > 1:
                return lines[1]  # Extracting the serial number if available
            else:
                return 'Serial number not found.'
        elif system == 'Linux':
            # Read product serial from the system file
            with open('/sys/class/dmi/id/product_serial') as file:
                return file.read().strip()
        elif system == 'Darwin':  # macOS
            # Retrieving serial number using system profiler
            return platform.system_profiler().get('serial_number', 'N/A')
        else:
            return 'Serial number retrieval not supported on this platform.'
    except Exception as e:
        return f'Error occurred: {str(e)}'

def get_computer_name():
    try:
        return platform.node()  # Retrieves the computer name
    except Exception as e:
        return f'Error occurred: {str(e)}'

# Get the computer name and serial number
computer_name = get_computer_name()
serial_number = get_serial_number()

print(f"Computer name: {computer_name}")
print(f"Serial number: {serial_number}")
