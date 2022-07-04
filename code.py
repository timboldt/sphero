# NOTE: This is still just a bunch of hacked-together code from various Adafruit examples.

import board
import displayio
import terminalio
import time

from adafruit_display_text import label
import adafruit_displayio_sh1107
from adafruit_servokit import ServoKit
import adafruit_vl53l4cd

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

displayio.release_displays()

i2c = board.I2C()

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_sh1107.SH1107(
    display_bus, width=WIDTH, height=HEIGHT, rotation=0
)

kit = ServoKit(channels=8)

vl53 = adafruit_vl53l4cd.VL53L4CD(i2c)
vl53.inter_measurement = 0
vl53.timing_budget = 200

print("VL53L4CD Simple Test.")
print("--------------------")
model_id, module_type = vl53.model_info
print("Model ID: 0x{:0X}".format(model_id))
print("Module Type: 0x{:0X}".format(module_type))
print("Timing Budget: {}".format(vl53.timing_budget))
print("Inter-Measurement: {}".format(vl53.inter_measurement))
print("--------------------")

vl53.start_ranging()

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

# Draw some label text
text1 = "0123456789ABCDEF123456789AB"  # overly long to see where it clips
text_area = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=8)
splash.append(text_area)
text2 = "SH1107"
text_area2 = label.Label(
    terminalio.FONT, text=text2, scale=2, color=0xFFFFFF, x=9, y=44
)
splash.append(text_area2)

pitch = 90
yaw = 90

while True:
    while not vl53.data_ready:
        pass
    vl53.clear_interrupt()
    text_area.text = "Distance: {} cm".format(vl53.distance)
    kit.servo[0].angle = pitch
    kit.servo[1].angle = yaw
    yaw = yaw + 10
    if yaw > 180:
        yaw = 0