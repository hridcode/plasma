print("Starting")

import board, busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.hid import HIDModes
from kmk.extensions.display import Display, TextEntry, ImageEntry
from kmk.extensions.display.ssd1306 import SSD1306
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.scanners import gpio

keyboard = KMKKeyboard()

layers = Layers()
split = Split(split_type=SplitType.BLE, split_side=SplitSide.LEFT)
i2c_bus = busio.I2C(board.GP4, board.GP5)

driver = SSD1306(
    i2c=i2c_bus,
    device_address=0x3C,
)

display = Display(
    display=driver,
    width=128
    height=64,
    brightness=0.8,
    brightness_step=0.1,
    dim_time=60,
    dim_target=0.1,
    off_time=180,
    powersave_dim_time=30,
    powersave_dim_target=0.1,
    powersave_off_time=90
)

display.entries = [
    TextEntry(text="the best keyboard", x=0, y=0)
]

keyboard.modules.append(layers)
keyboard.extensions.append(display)
keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
encoder_handler.pins = [(board.GP17, board.GP18, board.GP19),]
encoder_handler.map = [((KC.AUDIO_VOL_DOWN,KC.AUDIO_VOL_UP,KC.AUDIO_MUTE),),(KC.BRIGHTNESS_DOWN,KC.BRIGHTNESS_UP,KC.NO)]
keyboard.extensions.append(encoder_handler)
keyboard.modules.append(split)

keyboard.row_pins = (
    board.GP0, board.GP1, board.GP2, board.GP6, board.GP14
)

keyboard.col_pins = (
    board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12
)

keyboard.diode_orientation = DiodeOrientation.COL2ROW

MO1 = KC.MO(1)

keyboard.keymap = [
    [
        KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSPC,
        KC.Y, KC.U, KC.I, KC.O, KC.P, KC.BSLS,
        KC.H, KC.J, KC.K, KC.L, KC.ENTER, KC.NO,
        KC.N, KC.M, KC.COMM, KC.DOT, KC.UP, KC.SLSH,
        MO1, KC.NO, KC.NO, KC.LEFT, KC.DOWN, KC.RIGHT,
    ],
    [
        KC.F7, KC.F8, KC.F9, KC.F10, KC.MINS, KC.EQL,
        KC.F11, KC.F12, KC.NO, KC.LBRC, KC.RBRC,
        KC.PCSR, KC.NO, KC.NO, KC.SCLN, KC.QUOT,
        KC.SHIFT, KC.NO, KC.NO, KC.NO, KC.NO,
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO
    ]
]

thumb = gpio.GPIOInputPin(12)
keyboard.coord_mapping = {
    thumb: KC.SPACE
}

if __name__ == '__main__':
    keyboard.go()
    keyboard.go(hid_type=HIDModes.BLE, ble_name='hrid\'s split keyboard')