from mitmproxy import http
from mitmproxy.script import concurrent
from time import sleep
from gpiozero import RotaryEncoder, PWMOutputDevice, LED
import serial

class Delayer:
    def __init__(self):
        self.time = 0
        self.uart = serial.Serial('/dev/ttyACM0', 9600, timeout=10)
        self.uart.reset_input_buffer()
        self.encoder = RotaryEncoder(23, 24, max_steps=60)
        self.encoder.steps = 0
        self.fan = PWMOutputDevice(19, active_high=True, initial_value=0.25)
        self.LED = LED(pin=16, initial_value=False)
    
    def response(self, httpFlow):
        httpFlow.intercept()
        hostname = httpFlow.request.pretty_host
        print(hostname)
        if 'chatgpt.com' in hostname:
            self.LED.blink(on_time=0.1, off_time=0.1)
            # print(self.encoder.steps)
            # print("enter seconds to delay")
            # self.time = int(input())
            speed = self.encoder.steps / 60 * 100 + 150
            if (speed < 150):
                speed = 150
            self.uart.write(str(round(speed, None)).encode('utf-8'))
            self.uart.reset_input_buffer()
            self.uart.reset_output_buffer()
            slider = "not done"
            while(slider != "done"):
                self.fan.value = self.encoder.steps / 60 * 0.75 + 0.25
                while(self.uart.in_waiting <= 0):
                    print('waiting slider')
                slider = self.uart.readline().decode('utf-8').rstrip()
                while(slider == ''):
                    slider = self.uart.readline().decode('utf-8').rstrip()
            self.LED.off()
        httpFlow.resume()

addons = [Delayer()]