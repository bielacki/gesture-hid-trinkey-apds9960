# Gesture HID Controller (APDS-9960 + Trinkey RP2040 QT)

Control your device with simple hand gestures (up, down, left, right). This project uses a **USB HID keyboard/mouse**, so it works out of the box — no drivers or apps required.

![APDS-9960 + Trinkey RP2040 QT gestures demo](docs/demo.gif)

## Features

- **Right/Left gestures**: switch virtual desktops/spaces (default mapping for macOS).
- **Up/Down gestures**: page up/down.
- **LED feedback**: blinks **green** when a gesture is read; **blue** when ide.
- **Customizable**: remap gestures to any `Keycode` combo (volume, media keys, shortcuts, etc.).
- **Cross-platform**: tested on macOS, Ubuntu, Windows, and Android (via OTG).

> **Why it works seamlessly**: [HID devices](https://en.wikipedia.org/wiki/Human_interface_device) communicate using the same protocol as standard keyboards and mice. This ensures your operating system recognizes it as a hardware keyboard, making it universally compatible.

## Hardware

- **APDS-9960 Gesture Sensor** ([Adafruit #3595](https://www.adafruit.com/product/3595))
- **Trinkey RP2040 QT** ([Adafruit #5056](https://www.adafruit.com/product/5056))
- **STEMMA QT / Qwiic Cable** ([Adafruit #4399](https://www.adafruit.com/product/4399))
- Optional: USB-A extension or OTG adapter for Android.

> **Note**: Any CircuitPython board with **native USB HID** and **I²C** support can be used. If your board lacks an onboard NeoPixel, comment out the LED code or attach one.

## CircuitPython libraries used

- `adafruit_apds9960` - driver for the APDS-9960 sensor; decodes gesture directions.
- `adafruit_hid` - Sends USB HID keyboard/mouse reports (`Keycode`, `Keyboard`, `Mouse`).
- `neopixel` - Controls the Trinkey’s onboard NeoPixels for status.
- `board`, `usb_hid`, `time` - Standard CircuitPython modules for pins/USB/timing.


## Setup

### 1. Flash CircuitPython

1. Download the latest CircuitPython UF2 for the **QT2040 Trinkey**: [https://circuitpython.org/board/adafruit_qt2040_trinkey/](https://circuitpython.org/board/adafruit_qt2040_trinkey/).
2. Enter bootloader mode: Hold **BOOT/BOOTSEL**, tap **RESET**, and release **BOOT/BOOTSEL** when the **RPI-RP2** drive appears.
3. Drag-and-drop the UF2 file onto the **RPI-RP2** drive. The board will reboot as **CIRCUITPY**.

> Recovery tip: if **CIRCUITPY** won’t show or looks corrupted, re-enter the bootloader and drag the CircuitPython UF2 again. As a last resort, use the board’s “nuke” UF2 from the [Adafruit guide](https://learn.adafruit.com/adafruit-trinkey-qt2040/circuitpython), then reinstall CircuitPython.

### 2. Install Libraries


1. Download the [CircuitPython Library Bundle](https://circuitpython.org/libraries) matching your CircuitPython version (e.g., 9.x vs 10.x) and unzip it.  
2. Copy these from the unzipped `lib/` into your board’s **CIRCUITPY/lib/** folder:
    - `adafruit_apds9960/` (folder) - APDS-9960 driver
    - `adafruit_hid/` (folder) - USB HID keyboard/mouse
    - `neopixel.mpy` (file) - status LED control

### 3. Add the Code

Copy `code.py` to the **CIRCUITPY** root folder. CircuitPython will run it automatically (or after a reset).

### 4. Connect the Hardware

- Plug the **APDS-9960** into the Trinkey’s **STEMMA QT** port using a STEMMA QT/Qwiic cable.
- For boards without STEMMA QT, wire: **VIN→3V**, **GND→GND**, **SDA→SDA**, **SCL→SCL**.

### 5. Test It

1. Open a serial console (e.g., [Mu Editor](https://codewith.mu/en/download)).
2. Wave **right/left/up/down** to see messages like `gesture: right → next space` and LED feedback.

## Default Gesture Mapping

| Gesture | HID Action             | Use Case                     |
|---------|------------------------|------------------------------|
| Right   | `ctrl` + `→`          | Next Space/Desktop           |
| Left    | `ctrl` + `←`          | Previous Space/Desktop       |
| Down    | `PAGE_DOWN`           | Scroll down / Next page      |
| Up      | `PAGE_UP`             | Scroll up / Previous page    |

> Adjust mappings in `code.py` to match your OS shortcuts. You can find a full reference of HID actions here: [Keycode Reference](https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode).

## Customization

- **LEDs & Timing**
  ```python
  NUM_PIXELS = 1       # Set to 2 if your Trinkey has 2 NeoPixels
  cooldown = 0.15      # Seconds between gestures
  flash_time = 0.15    # LED flash duration
  ```

- **Key Mappings**
  ```python
  if g == 4:  # right
      press(Keycode.CONTROL, Keycode.RIGHT_ARROW)
  elif g == 3:  # left
      press(Keycode.CONTROL, Keycode.LEFT_ARROW)
  elif g == 2:  # down
      press(Keycode.PAGE_DOWN)
  elif g == 1:  # up
      press(Keycode.PAGE_UP)
  ```

- **Mouse Support**
  ```python
  # Example: Scroll on up/down gestures
  # mouse.move(0, 0, wheel=1)  # Scroll up
  ```

## Usage tips

- **Distance & orientation:** 5–15 cm above the sensor, straight on, works best.
- **Lighting:** very bright or reflective environments may reduce accuracy.
- **Debounce:** the `cooldown` prevents accidental double-triggers - tune to taste.
- **Pixels:** some Trinkey revisions have 2 NeoPixels. Set `NUM_PIXELS` accordingly.

## Troubleshooting

- **No response to gestures:**
  - Confirm libraries are in `CIRCUITPY/lib/`.
  - Use a **data** USB cable (not charge-only).
  - Check the serial console for debug messages.

- **Android issues:**
  - Ensure the device supports **USB-OTG** and use an OTG adapter.
  - Test gestures in a browser or document viewer.

- **Wrong gesture directions:**
  - Rotate the sensor or adjust mappings in `code.py`.

## Project Structure

```
.
├── code.py
├── lib/           # CircuitPython libraries
├── README.md
├── LICENSE
└── docs/
    ├── demo.gif
    └── wiring.md
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
