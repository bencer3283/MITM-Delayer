from gpiozero import RotaryEncoder, Button, PWMOutputDevice
from time import sleep

forward = PWMOutputDevice(18, active_high=True, initial_value=0.2)
backward = PWMOutputDevice(12, active_high=True, initial_value=0.2)

fan = PWMOutputDevice(19, active_high=True, initial_value=0.5)

knob = RotaryEncoder(23, 24, max_steps=60)

def PrintKnob(encoder):
    print(encoder.steps)
    # fan.value = encoder.steps / 60

def Forward():
    forward.on()
    sleep(0.01)
    forward.off()

def Backward():
    backward.on()
    sleep(0.01)
    backward.off()

if __name__ == "__main__":
    knob.when_rotated = PrintKnob
    # knob.when_rotated_clockwise = Forward
    # knob.when_rotated_counter_clockwise = Backward
    knobButton = Button(2, pull_up=True)
    while True:
        if knobButton.value == 1:
            knob.steps = 0
            print(knob.steps)
        # knob.wait_for_rotate()
        # print(knob.steps)

