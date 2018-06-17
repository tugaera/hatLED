# Example for rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)
#
# This is an example of how to use the SWIG-generated _rpi_ws281x module.
#
import time

import _rpi_ws281x as ws

# LED configuration.
LED_CHANNEL    = 0
LED_INTERVAL   = 0.25
LED_COUNT      = 32         # How many LEDs to light.
LED_FREQ_HZ    = 800000     # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM    = 10         # DMA channel to use, can be 0-14.
LED_GPIO       = 18         # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 128        # Set to 0 for darkest and 255 for brightest
LED_INVERT     = 0          # Set to 1 to invert the LED signal, good if using NPN
							# transistor as a 3.3V->5V level converter.  Keep at 0
							# for a normal/non-inverted signal.

# Define colors which will be used by the example. ).
DOT_COLORS = [  0x200000,   # red
				0x201000,   # orange
				0x202000,   # yellow
				0x002000,   # green
				0x002020,   # lightblue
				0x000020,   # blue
				0x100010,   # purple
				0x200010 ]  # pink


# Create a ws2811_t structure from the LED configuration.
# Note that this structure will be created on the heap so you need to be careful
# that you delete its memory by calling delete_ws2811_t when it's not needed.
leds = ws.new_ws2811_t()

# Initialize all channels to off
for channum in range(2):
    channel = ws.ws2811_channel_get(leds, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)

channel = ws.ws2811_channel_get(leds, LED_CHANNEL)

ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)

ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

# Initialize library with LED configuration.
resp = ws.ws2811_init(leds)
if resp != ws.WS2811_SUCCESS:
	message = ws.ws2811_get_return_t_str(resp)
	raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

# Wrap following code in a try/finally to ensure cleanup functions are called
# after library is initialized.
try:
	offset = 0
	flag = True
	while flag:
		# Update each LED color in the buffer.
		for i in range(LED_COUNT):
			# Pick a color based on LED position and an offset for animation.
			color = DOT_COLORS[(i + offset) % len(DOT_COLORS)]

			# Set the LED color buffer value.
			ws.ws2811_led_set(channel, i, color)

		# Send the LED color data to the hardware.
		resp = ws.ws2811_render(leds)
		if resp != ws.WS2811_SUCCESS:
			message = ws.ws2811_get_return_t_str(resp)
			raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))

		# Delay for a small period of time.
		time.sleep(LED_INTERVAL)

		# Increase offset to animate colors moving.  Will eventually overflow, which
		# is fine.
		offset += 1
		if offset == 5:
			flag = False

finally:
	# Ensure ws2811_fini is called before the program quits.
	ws.ws2811_fini(leds)
	# Example of calling delete function to clean up structure memory.  Isn't
	# strictly necessary at the end of the program execution here, but is good practice.
ws.delete_ws2811_t(leds)
