# Wiring & Hardware Notes

This project uses the **APDS-9960** gesture/proximity sensor with a **QT2040 Trinkey**. Connection is via **STEMMA QT/Qwiic** (JST-SH 4-pin), so it’s plug-and-play.

> TL;DR: If you have a STEMMA QT/Qwiic port on your board, just plug the cable in. If not, wire 3V, GND, SDA, SCL directly.

---

## STEMMA QT / Qwiic (recommended)

- **Cable:** STEMMA QT / Qwiic (JST-SH 4-pin)
- **Signals:** 3V • GND • SDA • SCL
- **Address:** `0x39` (APDS-9960 default)
- **Orientation:** sensor window faces your hand

With the QT2040 Trinkey, use the on-board **STEMMA QT** port. No soldering required.

---

## Direct wiring (no QT/Qwiic port)

Wire the APDS-9960 breakout to your board’s I²C pins:

| APDS-9960 breakout | Microcontroller board |
|---|---|
| VIN | 3V (3.3 V) |
| GND | GND |
| SDA | SDA (I²C data) |
| SCL | SCL (I²C clock) |
| INT *(optional)* | Any GPIO (not used by the default code) |

> The Adafruit APDS-9960 breakout is 3–5 V friendly. The sensor itself is 3.3 V; the breakout handles the level shifting/regulation.

---

## Power & placement tips

- **Range:** ~5–15 cm above the sensor works best.
- **Lighting:** Strong IR from sunlight/glossy surfaces can reduce accuracy.
- **Mounting:** Keep the sensor window unobstructed; avoid recessing it too deep in an enclosure.

---

## I²C sanity check

If gestures aren’t detected, verify the sensor appears on the I²C bus (should be `0x39`). Drop this into a quick `i2c_scan.py`:

```python
import board, busio
i2c = busio.I2C(board.SCL, board.SDA)
while not i2c.try_lock():
    pass
addrs = [hex(x) for x in i2c.scan()]
i2c.unlock()
print("i2c addresses:", addrs)
```

You should see `0x39` in the printed list.

---

## Using other boards

The README examples use **QT2040 Trinkey**, but any **CircuitPython** board with **native USB (HID)** and **I²C** will work (e.g., **Adafruit QT Py ESP32-S2**, **QT Py RP2040**, **Feather RP2040**). If your board lacks an onboard NeoPixel, either comment out the LED code or attach an external NeoPixel to a free pin.

