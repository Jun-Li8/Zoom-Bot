import win32gui
import re
from mute import controlKeyboard
from pynput.keyboard import Key, Controller
import time
from threading import Timer
# from mute import type_chat

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def type_chat(s):
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')
    time.sleep(0.25)
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')
    if s == 'start':
        keyboard.type('+Convoz has been initialed')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    else:
        keyboard.type('Ending +Convoz')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(0.5)
        keyboard.type('An email will be sent shortly')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

warnings = {'personal_attack': 'Remember to be mindful of how you communicate. Criticism is valuable as long as it is done in a constructive and professional manner.',
            'bigotry': 'Remember to be open minded of other perspectives and beliefs.',
            'profanity': 'Remember to use language that is appropriate for a professional environment', 
            'sexual_advances': 'Remember that a professional environment is not a place for your personal affairs.', 
            'criminal_activity': 'Remember that any attempts of violent or criminal behavior will be subjected to disciplinary action.', 
            'adult_only': 'Remember of mindful of your language and how it might causes discomfortable amongst the people around you.', 
            'mental_issues':'Remember to check up on classmates/teammates occasionally. Being a supportive and encourging member can greatly improve your working environment.'}

def warn_bully(btype):
    keyboard = Controller()
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')
    time.sleep(0.25)
    with keyboard.pressed(Key.alt):
        keyboard.press('h')
        keyboard.release('h')
    if btype in warnings:
        keyboard.type(warnings[btype])
    else:
        keyboard.type('Remember to be mindful of how your behavior and language can affect your relationship with your teammates and environment.')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def bot(s): 
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
            if "zoom" in i[1].lower():
                # print(i)
                # win32gui.ShowWindow(i[0],5)
                win32gui.SetForegroundWindow(i[0])
                # controlKeyboard()
                type_chat(s)
                break
    # print(top_windows)

def warn(btype,lol): 
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
            if "zoom" in i[1].lower():
                win32gui.SetForegroundWindow(i[0])
                warn_bully(btype)
                break
    # print(top_windows)