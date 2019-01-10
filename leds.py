import time

from neopixel import *

# LED strip configuration:
LED_0_COUNT = 60  # Number of LED pixels.
LED_0_PIN = 18  # GPIO pin connected to the pixels (must support PWM! GPIO 13 and 18 on RPi 3).
LED_0_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_0_DMA = 10  # DMA channel to use for generating signal (Between 1 and 14)
LED_0_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_0_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_0_CHANNEL = 0  # 0 or 1
LED_0_STRIP = ws.SK6812_STRIP_GRBW

LED_1_COUNT = 44  # Number of LED pixels.
LED_1_PIN = 13  # GPIO pin connected to the pixels (must support PWM! GPIO 13 or 18 on RPi 3).
LED_1_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_1_DMA = 11  # DMA channel to use for generating signal (Between 1 and 14)
LED_1_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_1_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_1_CHANNEL = 1  # 0 or 1
LED_1_STRIP = ws.WS2811_STRIP_GRB

initialized = False
strip1 = None
strip2 = None


def init():
    global strip1, strip2, initialized
    # Create NeoPixel objects with appropriate configuration for each strip.
    strip1 = Adafruit_NeoPixel(LED_0_COUNT, LED_0_PIN, LED_0_FREQ_HZ, LED_0_DMA, LED_0_INVERT, LED_0_BRIGHTNESS,
                               LED_0_CHANNEL, LED_0_STRIP)
    strip2 = Adafruit_NeoPixel(LED_1_COUNT, LED_1_PIN, LED_1_FREQ_HZ, LED_1_DMA, LED_1_INVERT, LED_1_BRIGHTNESS,
                               LED_1_CHANNEL, LED_1_STRIP)

    # Initialize the library (must be called once before other functions).
    strip1.begin()
    strip2.begin()

    # Black out any LEDs that may be still on for the last run
    blackout(strip1)
    blackout(strip2)

    initialized = True


# Turn all LEDs on a strip black / turn off
def blackout(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()


def update(monitor, colors):
    global strip1, strip2
    if not initialized:
        init()
    if monitor == 0:
        if len(colors) != LED_0_COUNT:
            print('Request to monitor ' + str(monitor) + ' has unequal amounts of LEDs installed than described in the '
                  'server configuration (received: ' + str(len(colors)) + ', expected: ' + str(LED_0_COUNT) + ')')
            return
        for i in range(strip1.numPixels()):
            strip1.setPixelColor(i, colors[i])
        strip1.show()
    elif monitor == 1:
        if len(colors) != LED_1_COUNT:
            print('Request to monitor ' + str(monitor) + ' has unequal amounts of LEDs installed than described in the '
                  'server configuration (received: ' + str(len(colors)) + ', expected: ' + str(LED_1_COUNT) + ')')
            return
        for i in range(strip2.numPixels()):
            strip2.setPixelColor(i, colors[i])
        strip2.show()
