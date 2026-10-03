import board
import neopixel
import time

NUM_PIXELS = 7
PIXEL_PIN = board.D18   # GPIO 18

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=0.3,
    auto_write=True
)

def blinkIn():
    for flashes in range(5):
        pixels.fill((0, 255, 0))
        time.sleep(0.5)
        
        pixels.fill((0, 0, 0))
        time.sleep(0.5)

def blinkOut():
    for flashes in range(5):
        pixels.fill((255, 0, 0))
        time.sleep(0.5)
        
        pixels.fill((0, 0, 0))
        time.sleep(0.5)