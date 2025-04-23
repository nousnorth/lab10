import asyncio
import shelve
from time import sleep, strftime, gmtime

from bleak import BleakScanner

KNOWN_DEVICES = {
    "Unknown 1": "54:94:94:0E:2B:70",
    "Unknown 2": "48:E0:64:FA:5D:54",
    "Unknown 3": "1C:AF:4A:5B:C6:9D",
    "Tintin (Cellphone)": "62:E9:4B:C5:C0:62"
}

def log_devices(devices):
    with shelve.open("device_log") as db:
        for name, address in devices.items():
            key = name + '_' + address
            formatted_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            if key in db:
                time_list = db[key]
                time_list.append(formatted_time)
                db[key] = time_list
            else:
                db[key] = [formatted_time]
    print("Logged devices in the shelf database.")

async def check_for_known_devices():
    devices = await BleakScanner.discover()
    nearby_known_devices = {}

    for device in devices:
        if device.address in KNOWN_DEVICES.values():
            device_name = [name for name, addr in KNOWN_DEVICES.items() if addr == device.address][0]
            print(f"{device_name} is nearby!")
            nearby_known_devices[device_name] = device.address

    return nearby_known_devices

async def scan_for_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover(timeout=10.0)
    for device in devices:
        print(f"Device Name: {device.name}, Address: {device.address}")
    return devices

async def scan():
    nearby_devices = await check_for_known_devices()
    if nearby_devices:
        log_devices( nearby_devices )
    else:
        print( "No known devices nearby." )


def main():
    # asyncio.run( scan_for_devices() )
    while True:
        print("Scanning...")
        asyncio.run( scan() )
        print("sleeping till next loop...")
        sleep(15)
        print("Verifying log...")
        with shelve.open("device_log") as db:
            for name, address in db.items():
                print(f"{name}: {address}")

if __name__ == '__main__':
    main()

asyncio.run(check_for_known_devices())
