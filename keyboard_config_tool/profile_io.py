import json
from pathlib import Path
from .models import KeyboardProfile, Layer, KeyAction, RGBConfig

def save_profile(path: Path, profile: KeyboardProfile) -> None:
    data = {
        "layout_name": profile.layout_name,
        "layers": [
            {
                "name": layer.name,
                "keys": {str(idx): {"code": ka.code, "label": ka.label}
                         for idx, ka in layer.keys.items()}
            }
            for layer in profile.layers
        ],
        "rgb": {
            "mode": profile.rgb.mode,
            "brightness": profile.rgb.brightness,
            "speed": profile.rgb.speed,
            "color": list(profile.rgb.color),
        },
    }
    path.write_text(json.dumps(data, indent=2))

def load_profile(path: Path) -> KeyboardProfile:
    data = json.loads(path.read_text())
    layers = []
    for layer_data in data["layers"]:
        keys = {
            int(idx): KeyAction(code=v["code"], label=v["label"])
            for idx, v in layer_data["keys"].items()
        }
        layers.append(Layer(name=layer_data["name"], keys=keys))
    rgb = RgbConfig(
        mode=data["rgb"]["mode"],
        brightness=data["rgb"]["brightness"],
        speed=data["rgb"]["speed"],
        color=tuple(data["rgb"]["color"]),
    )
    return KeyboardProfile(
        layout_name=data["layout_name"],
        layers=layers,
        rgb=rgb,
    )