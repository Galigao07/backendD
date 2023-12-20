import uuid

def get_mac_address():
    mac = uuid.getnode()
    return ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(40, -1, -8)])

# Get the MAC address
mac_address = get_mac_address()
print("MAC Address:", mac_address)
from django.utils import timezone

current_datetime = timezone.now()

# Extracting date and time separately
current_date = current_datetime.date()  # Extracts the date
current_time = current_datetime.time()  # Extracts the time

print("Current Date:", current_date)
print("Current Time:", current_time)