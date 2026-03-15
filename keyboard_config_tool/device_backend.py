from abc import ABC, abstractmethod
from typing import List
from .models import KeyboardProfile

class DeviceBackend(ABC):
    @abstractmethod
    def list_devices(self) -> List[str]:
        """List available devices."""
        pass

    @abstractmethod
    def connect(self, device_id: str) -> bool:
        """Connect to a device by its ID."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the current device."""
        pass

    @abstractmethod
    def get_profile(self) -> KeyboardProfile:
        """Read the current profile from the device."""
        pass

    @abstractmethod
    def apply_profile_preview(self, profile: KeyboardProfile) -> None:
        """Apply a profile preview to the device without saving."""
        pass

    @abstractmethod
    def save_profile(self, profile: KeyboardProfile) -> None:
        """Save a profile to the device."""
        pass