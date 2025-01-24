import asyncio
from bleak import BleakScanner, BleakClient

class BleTools:
    def __init__(self, service_uuid, characteristic_uuid):
        self.service_uuid = service_uuid
        self.characteristic_uuid = characteristic_uuid

    async def find_device_by_service_uuid(self):
        devices = await BleakScanner.discover()
        for device in devices:
            if self.service_uuid.lower() in [str(uuid).lower() for uuid in device.metadata.get("uuids", [])]:
                print(f"Found device: {device.name} with address: {device.address}")
                if (device.name == "DogMonitor"): # 하필 같은 서비스 UUID를 가지고 있어서...
                    continue 
                return device.address
        return None

    async def send_message(self, message):
        address = await self.find_device_by_service_uuid()
        if address is None:
            print("No device found with the given service UUID.")
            return

        async with BleakClient(address) as client:
            message_bytes = message.encode("utf-8")
            await client.write_gatt_char(self.characteristic_uuid, message_bytes)
            print(f"Message sent to {address}: {message}")
    
    def send_message_sync(self, message):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message(message))
