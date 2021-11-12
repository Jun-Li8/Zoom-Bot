from pynput.keyboard import Key, Controller
import time

def controlKeyboard():
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press('a')
        keyboard.release('a')

def type_chat():
    print('nice')
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')
    keyboard.type('Jun is a BULLY')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(0.1)
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')

# type_chat()
