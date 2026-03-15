from typing import List, Optional
from .device_backend import DeviceBackend
from .models import KeyboardProfile

class HidBackend(DeviceBackend):
    def __init__(self):
        self._connected = False
        self._profile: Optional[KeyboardProfile] = None
    
    def list_devices(self) -> List[str]:
        #TODO: use hidapi to enumerate real devices
        return []

    def connect(self, identifier: str) -> bool:
        #TODO: open HID device by VID/PID
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def get_profile(self) -> KeyboardProfile:
        if not self._connected:
            raise RuntimeError("Not connected")
        if not self._profile:
            raise RuntimeError("No profile loaded")
        return self._profile

    def apply_profile_preview(self, profile: KeyboardProfile) -> None:
        if not self._connected:
            raise RuntimeError("Not connected")
        #TODO: send VIA-compatible HID packets
        self._profile = profile

    def save_profile(self, profile: KeyboardProfile) -> None:
        if not self._connected:
            raise RuntimeError("Not connected")
        #TODO: send save-to-flash command
        self._profile = profile