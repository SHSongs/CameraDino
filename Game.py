from pynput.keyboard import Key, Controller
import time

keyboard = Controller()


def press_space():
    keyboard.press(Key.space)
    keyboard.release(Key.space)

time.sleep(1)

press_space()

time.sleep(3)

press_space()