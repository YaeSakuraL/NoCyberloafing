import pyautogui
import time
import keyboard
import sys
import os
import pygame
from glob import glob
import random
import threading

def init():
    pygame.mixer.init()
    os.system('cls')
    print('Welcome to Cyberloafing Detector~♪')
    print('Max cyberloafing time(seconds)~♪:', end=' ')
    global max_cyberloafing_time
    max_cyberloafing_time = int(input()) * 10
    print('Max working time(seconds)~♪:', end=' ')
    global max_working_time
    max_working_time = int(input()) * 10

    global focus_window
    window_list = get_windows()
    focus_window = []

    os.system('cls')
    for i in range(len(window_list)):
        print(i, window_list[i].title)
    print('Select the window you want to focus on~♪')
    index = int(input())
    focus_window.append(window_list[index])
    while True:
        os.system('cls')
        for i in range(len(window_list)):
            if window_list[i] in focus_window:
                #print in purple
                print('\033[35m', end='')
                print(">", i, window_list[i].title)
                print('\033[0m', end='')
            else:
                print(i, window_list[i].title)
        print('Select the window you want to focus on, press 999 to finish selecting~♪')
        index = int(input())  
        if index == 999:
            break

        if window_list[index] in focus_window:
            focus_window.remove(window_list[index])
        else:
            focus_window.append(window_list[index])

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
    cyberloafing_flag = False
    while True:
        time.sleep(0.1)
        for window in focus_window:
            if window.isActive:
                cyberloafing_flag = False
                break
            else:
                cyberloafing_flag = True
        if cyberloafing_flag:
            cyberloafing_count = 0
            working_count += 1
            print('Working hard~♪',end='\r')
            sys.stdout.flush()
            if working_count % max_working_time == 0:
                try:
                    voice = random.choice(working_voice).replace('\\','/')
                    pygame.mixer.music.load(voice)
                    pygame.mixer.music.play()
                except:
                    #No voice
                    pass
        else:
            working_count = 0
            cyberloafing_count += 1
            print('Cyberloafing~♪',end='\r')
            sys.stdout.flush()
            if cyberloafing_count % max_cyberloafing_time == 0:
                try:
                    voice = random.choice(cyberloafing_voice).replace('\\','/')
                    pygame.mixer.music.load(voice)
                    pygame.mixer.music.play()
                except:
                    #No voice
                    pass
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
    init()

    os.system('cls')
    print('Start focusing~♪')
    print('Press \'Ecs\' to exit~♪')

    stop_threads = False
    

    t1 = threading.Thread(target=check_foreground)
    t2 = threading.Thread(target=exit)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
