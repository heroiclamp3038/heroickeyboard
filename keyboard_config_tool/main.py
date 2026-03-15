import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QColorDialog, QFileDialog
)
from PySide6.QtGui import QColor

from .mock_backend import MockBackend
from .models import KeyboardProfile, KeyPosition, KeyAction
from .profile_io import save_profile, load_profile

class KeyboardEditor(QWidget):
    def __init__(self, backend: MockBackend):
        super().__init__()
        self.backend = backend
        self.backend.connect("Mock Device 1")
        self.profile: KeyboardProfile = self.backend.get_profile()
        self.current_layer_index = 0

        self.setWindowTitle("HeroicConfigure: The One and Only Configuration Tool for the HeroicKeyboard")

        main_layout = QVBoxLayout(self)

        # Layer selector
        layer_row = QHBoxLayout()
        layer_row.addWidget(QLabel("Layer:"))
        self.layer_combo = QComboBox()
        for layer in self.profile.layers:
            self.layer_combo.addItem(layer.name)
        self.layer_combo.currentIndexChanged.connect(self.on_layer_changed)
        layer_row.addWidget(self.layer_combo)
        main_layout.addLayout(layer_row)

        # Keyboard grid
        self.grid = QGridLayout()
        main_layout.addLayout(self.grid)
        self.key_buttons: dict[int, QPushButton] = {}
        self._build_keyboard_grid()

        # Key action editor
        action_row = QHBoxLayout()
        action_row.addWidget(QLabel("Selected key:"))
        self.selected_key_label = QLabel("-")
        action_row.addWidget(self.selected_key_label)

        action_row.addWidget(QLabel("Keycode:"))
        self.keycode_combo = QComboBox()
        # Minimal set of keycodes for now
        for code in ["KC_NO", "KC_A", "KC_B", "KC_C", "KC_ENTER", "KC_ESC", "KC_SPACE"]:
            self.keycode_combo.addItem(code)
        self.keycode_combo.currentIndexChanged.connect(self.on_keycode_changed)
        action_row.addWidget(self.keycode_combo)

        main_layout.addLayout(action_row)

        # RGB controls
        rgb_row = QHBoxLayout()
        rgb_row.addWidget(QLabel("RGB Color:"))
        self.rgb_color_label = QLabel()
        self.rgb_color_label.setAutoFillBackground(True)
        rgb_row.addWidget(self.rgb_color_label)
        self.rgb_button = QPushButton("Pick Color")
        self.rgb_button.clicked.connect(self.on_pick_color)
        rgb_row.addWidget(self.rgb_button)
        main_layout.addLayout(rgb_row)

        # Save/load buttons
        file_row = QHBoxLayout()
        self.save_btn = QPushButton("Save Profile")
        self.save_btn.clicked.connect(self.on_save_profile)
        file_row.addWidget(self.save_btn)
        self.load_btn = QPushButton("Load Profile")
        self.load_btn.clicked.connect(self.on_load_profile)
        file_row.addWidget(self.load_btn)
        main_layout.addLayout(file_row)

        self.selected_key_index: Optional[int] = None
        self._update_rgb_label()

    def _build_keyboard_grid(self):
        layout = self.backend._layout  # using mock's layout
        for kp in layout.keys:
            btn = QPushButton("")
            btn.setFixedSize(int(40 * kp.w), int(40 * kp.h))
            btn.clicked.connect(lambda _, idx=kp.index: self.on_key_clicked(idx))
            self.grid.addWidget(btn, int(kp.y), int(kp.x))
            self.key_buttons[kp.index] = btn
        self._refresh_key_labels()

    def _refresh_key_labels(self):
        layer = self.profile.layers[self.current_layer_index]
        for idx, btn in self.key_buttons.items():
            action = layer.keys.get(idx)
            if action and action.code != "KC_NO":
                btn.setText(action.label or action.code)
            else:
                btn.setText("")

    def on_layer_changed(self, index: int):
        self.current_layer_index = index
        self._refresh_key_labels()

    def on_key_clicked(self, index: int):
        self.selected_key_index = index
        self.selected_key_label.setText(str(index))
        layer = self.profile.layers[self.current_layer_index]
        action = layer.keys.get(index)
        if action:
            idx = self.keycode_combo.findText(action.code)
            if idx >= 0:
                self.keycode_combo.setCurrentIndex(idx)

    def on_keycode_changed(self, _):
        if self.selected_key_index is None:
            return
        code = self.keycode_combo.currentText()
        layer = self.profile.layers[self.current_layer_index]
        layer.keys[self.selected_key_index] = KeyAction(code=code, label=code)
        self._refresh_key_labels()
        self.backend.apply_profile_preview(self.profile)

    def _update_rgb_label(self):
        r, g, b = self.profile.rgb.color
        color = QColor(r, g, b)
        palette = self.rgb_color_label.palette()
        palette.setColor(self.rgb_color_label.backgroundRole(), color)
        self.rgb_color_label.setPalette(palette)

    def on_pick_color(self):
        r, g, b = self.profile.rgb.color
        initial = QColor(r, g, b)
        color = QColorDialog.getColor(initial, self, "Pick RGB Color")
        if color.isValid():
            self.profile.rgb.color = (color.red(), color.green(), color.blue())
            self._update_rgb_label()
            self.backend.apply_profile_preview(self.profile)

    def on_save_profile(self):
        path_str, _ = QFileDialog.getSaveFileName(self, "Save Profile", "", "JSON Files (*.json)")
        if not path_str:
            return
        save_profile(Path(path_str), self.profile)

    def on_load_profile(self):
        path_str, _ = QFileDialog.getOpenFileName(self, "Load Profile", "", "JSON Files (*.json)")
        if not path_str:
            return
        self.profile = load_profile(Path(path_str))
        # Rebuild layer combo
        self.layer_combo.clear()
        for layer in self.profile.layers:
            self.layer_combo.addItem(layer.name)
        self.current_layer_index = 0
        self._refresh_key_labels()
        self._update_rgb_label()
        self.backend.apply_profile_preview(self.profile)

def main():
    app = QApplication(sys.argv)
    backend = MockBackend()
    w = KeyboardEditor(backend)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
