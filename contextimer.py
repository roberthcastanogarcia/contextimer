#!/usr/bin/env python3

import time
import os
import math
from datetime import datetime
from datetime import timedelta
import sys
import subprocess

#Modify in order to read any path file
def read_state():
    f = open('time.txt', 'r')
    level = int(f.readline())
    f.close()
        
    return level

def get_number_of_jobs(ncontexts):
    njobs = 0
    for i in range(1, ncontexts + 1):
        njobs = njobs + i
    return njobs

def read_contexts():
    f = open('contexts.txt', 'r')
    n = int(f.readline())
    contexts = []
    
    for i in range(1, n + 1):
        contexts.append(f.readline().replace("\n",""))
    
    f.close()
    return contexts
    

#Countdown function
def countdown(n):
    while n >= 0:
        if n <= 10:
            os.system("espeak " + str(n) + " &")	
        print(timedelta(seconds=(n)))
        time.sleep(1)
        n = n - 1
    return True

def voice(voice_command):
    if voice_command == "work":
        os.system("aplay whistle.wav -q &")
    elif voice_command == "cooldown":
        os.system("aplay school_bell.wav -q &")
    elif voice_command == "rest":
        os.system("espeak 'Get some rest' &")
        os.system("aplay school_bell.wav -q &")
    elif voice_command == "getReady":
        os.system("espeak 'Get ready!' &")

def stat_messages(level, status, njobs):
    print("Nivel: " + str(level), end="\t")
    if status == "work":
        print("Duracion: " + str( timedelta(seconds=level) ))
    elif status == "cooldown":
        print("Duracion: " + str( timedelta( seconds=round(level/4) )))
    elif status == "rest":
        print("Duracion: " + str( timedelta( seconds=round((level*njobs) / 2 ))))

#main function
def contextimer():
    level = read_state()
    contexts = read_contexts()
    ncontexts = len(contexts)
    njobs = get_number_of_jobs(ncontexts)
    context_reach = ncontexts
    
    while True:
        
        context_reach = ncontexts
        voice("getReady")
        countdown(3)
        
        for i in range(0, ncontexts):
            for j in range(0,context_reach):
                
                print("Working: ", contexts[(ncontexts-1) - j])
                stat_messages(level, "work", njobs)
                os.system("espeak '" + str(contexts[(ncontexts-1) - j]) + "'")
                voice("work")
                countdown(level)
                
                print("Cooldown: ", contexts[(ncontexts-1) - j])
                stat_messages(level, "cooldown", njobs)
                voice("cooldown")
                countdown(round(level/4))
                
            context_reach = context_reach - 1
        
        voice("rest")
        print("Rest")
        stat_messages(level, "rest", njobs)
        countdown(round((level*njobs)/2))
        
        level = level + 1

def main():
    contextimer()
    
if __name__ == "__main__":
    main()
