import time, board, usb_hid
import neopixel
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

# --- LEDs (Trinkey QT2040 onboard NeoPixels) ---
NUM_PIXELS = 1  # QT2040 Trinkey has 1; if yours has 1, set to 2
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=True)

BLUE = (0, 0, 50)
GREEN = (0, 50, 0)


def set_all(color):
    pixels.fill(color)


i2c = board.I2C()
apds = APDS9960(i2c)

apds.enable_proximity = True
apds.enable_gesture = True

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)


def press(*keys):
    kbd.press(*keys)
    kbd.release_all()


last = 0.0
cooldown = 0.15  # seconds between accepted gestures
flash_time = 0.15  # how long to show green after a gesture

# start in standby color
set_all(BLUE)

while True:
    g = apds.gesture()  # 0 none, 1 up, 2 down, 3 left, 4 right
    now = time.monotonic()

    if g and now - last > cooldown:
        set_all(GREEN)  # active: gesture detected

        if g == 4:
            print("gesture: right → next space")
            press(Keycode.CONTROL, Keycode.RIGHT_ARROW)
        elif g == 3:
            print("gesture: left → prev space")
            press(Keycode.CONTROL, Keycode.LEFT_ARROW)
        elif g == 1:
            print("gesture: up → PAGE_UP")
            # press(Keycode.CONTROL, Keycode.UP_ARROW)
            press(Keycode.PAGE_UP)
        elif g == 2:
            print("gesture: up → PAGE_DOWN")
            # press(Keycode.CONTROL, Keycode.DOWN_ARROW)
            press(Keycode.PAGE_DOWN)

        last = now
        # keep green briefly so you can see it, then back to standby blue
        time.sleep(flash_time)
        set_all(BLUE)
