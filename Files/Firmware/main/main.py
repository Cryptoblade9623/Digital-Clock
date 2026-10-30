#importing all the required libraries
from machine import Pin,I2C
import rp2
import neopixel
import tm1637
import time
import machine
import RTC_DS3231

#define the pins for the RTC and display
RTC_SDA_PIN = 14
RTC_SCL_PIN = 15
DISPLAY_CLK_PIN = 12
DISPLAY_DIO_PIN = 13

#initialize the neopixel, I2C, display, and RTC
np = neopixel.NeoPixel(machine.Pin(29), 20)
rtc_i2c = I2C(1, sda=Pin(RTC_SDA_PIN), scl=Pin(RTC_SCL_PIN), freq=400000)
display = tm1637.TM1637(clk=Pin(DISPLAY_CLK_PIN), dio=Pin(DISPLAY_DIO_PIN))
rtc = RTC_DS3231.DS3231(rtc_i2c)

#get the time from the ds3231 and disaply it on the tm1637 and neopixels
while True:
    current_time = rtc.get_time()
    #convert the time to hour, minute and second variables
    hour = current_time[4]
    minute = current_time[5]
    second = current_time[6]

    #formatting and displaying on the tm163
    display_time = "{:02d}{:02d}".format(current_time[4], current_time[5])
    display.show(display_time)

    #make the cycle for neopixels and a smoothe fade
    active_led = current_time[6] // 3
    ms_cycle = (time.ticks_ms() % 3000) / 3000.0
    smooth_brightness = int(ms_cycle * 255)
    for i in range(20):
        if i == active_led:
            np[i] = (smooth_brightness, 0, 0)
        else:
            np[i] = (0, 0, 10)

    np.write()

    #set refresh rate to 25m
    time.sleep_ms(25)