from typing import List
from .device_backend import DeviceBackend
from .models import (KeyboardProfile, KeyboardLayout, Layer, KeyAction, RGBConfig, KeyPosition)

class MockBackend(DeviceBackend):
    def __init__(self):
        self._connected = False

        self._layout = KeyboardLayout(
            name="Mock Layout",
            keys=[
                KeyPosition(x=0, y=0, index=0),
                KeyPosition(x=1, y=0, index=1)
            ]
        )

        base_layer = Layer(
            name="Base",
            keys={
                0: KeyAction(code="KC_A", label="A"),
                1: KeyAction(code="KC_B", label="B")
            }
        )

        fn_layer = Layer(
            name="Fn",
            keys = {
                0: KeyAction(code="KC_C", label="C"), 
                1: KeyAction(code="KC_D", label="D")
            }
        )

        self._profile = KeyboardProfile(
            layout_name = self._layout.name,
            layers=[base_layer, fn_layer],
            rgb=RGBConfig(mode="static", brightness=128, speed=128, color=(255, 255, 255))
        )

        self._connected_device = None


    def list_devices(self) -> List[str]:
        return ["Mock Device 1", "Mock Device 2"]

    def connect(self, device_id: str) -> bool:
        self._connected_device = device_id
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected_device = None
        self._connected = False

    def get_profile(self) -> KeyboardProfile:
        if not self._connected_device:
            raise Exception("No device connected")
        return self._profile

    def apply_profile_preview(self, profile: KeyboardProfile) -> None:
        if not self._connected_device:
            raise Exception("No device connected")
        print(f"Applying profile preview to {self._connected_device}: {profile}")
        self._profile = profile

    def save_profile(self, profile: KeyboardProfile) -> None:
        if not self._connected_device:
            raise Exception("No device connected")
        print(f"Saving profile to {self._connected_device}: {profile}")
        self._profile = profile