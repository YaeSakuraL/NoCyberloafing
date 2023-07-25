import pyautogui
import time
import keyboard
import sys
import os
import pygame
from glob import glob
import random
import threading

def get_windows():
    windows = []
    for x in pyautogui.getAllWindows():  
        if x.title != '':
            windows.append(x)
    return windows

def check_foreground():
    global focus_window
    global max_cyberloafing_time
    global max_working_time
    
    working_voice = glob('./voice/Working/*.wav')
    cyberloafing_voice = glob('./voice/Cyberloafing/*.wav')
    working_count = 0
    cyberloafing_count = 0
    while True:
        time.sleep(0.1)
        if focus_window.isActive:
            cyberloafing_count = 0
            working_count += 1
            print('Working hard~♪',end='\r')
            sys.stdout.flush()
            if working_count % max_working_time == 0:
                voice = random.choice(working_voice).replace('\\','/')
                pygame.mixer.music.load(voice)
                pygame.mixer.music.play()
        else:
            working_count = 0
            cyberloafing_count += 1
            print('Cyberloafing~♪',end='\r')
            sys.stdout.flush()
            if cyberloafing_count % max_cyberloafing_time == 0:
                voice = random.choice(cyberloafing_voice).replace('\\','/')
                pygame.mixer.music.load(voice)
                pygame.mixer.music.play()
        global stop_threads
        if stop_threads:
            break

def exit():
    while True:
        if keyboard.is_pressed('esc'):
            os.system('cls')
            global stop_threads
            stop_threads = True
            print('Exit~♪')
            break

if __name__ == '__main__':
    pygame.mixer.init()
    os.system('cls')
    print('Welcome to Cyberloafing Detector~♪')
    print('Max cyberloafing time(seconds)~♪:', end=' ')
    max_cyberloafing_time = int(input()) * 10
    print('Max working time(seconds)~♪:', end=' ')
    max_working_time = int(input()) * 10

    window_list = get_windows()
    for i in range(len(window_list)):
        print(i, window_list[i].title)
    print('Select the window you want to focus on~♪')
    index = int(input())
    focus_window = window_list[index]
    os.system('cls')
    print('Focus on the window:', focus_window.title, '~♪')
    print('Press \'Ecs\' to exit~♪')

    stop_threads = False
    

    t1 = threading.Thread(target=check_foreground)
    t2 = threading.Thread(target=exit)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
