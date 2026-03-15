from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

Keycode = str

@dataclass
class KeyAction:
    code: Keycode
    label: str

@dataclass
class KeyPosition:
    x: float
    y: float
    w: float = 1.0
    h: float = 1.0
    index: int = 0

@dataclass
class Layer:
    name: str
    keys: Dict[int, KeyAction] = field(default_factory=dict)

@dataclass
class RGBConfig:
    mode: str = 'static'
    brightness: int = 128
    speed: int = 128
    color: Tuple[int, int, int] = (255, 255, 255)

@dataclass
class KeyboardLayout:
    name: str
    keys: List[KeyPosition]

@dataclass
class KeyboardProfile:
    layout_name: str
    layers: List[Layer]
    rgb: RGBConfig