"""script to act as a bridge between an Xbox360 controller and LIRC"""

import time
from evdev import InputDevice, ecodes
from select import select
from . import *

def main():    
    dev = InputDevice('/dev/input/event0')
    done=False
    debounce = {}
    #clear out old repeating commands, in case of previous failure
    for cmd in repeating_commands.keys():
        lirc_send(cmd,stop=True)

    while not done:
       r,w,x = select([dev], [], [])
       for event in dev.read():
           if event.type==0 and event.code==0 and event.value==0:
               continue;
           key = '%04d%04d'%(event.code,event.type)
           try:
               if event.value!=0 and debounce[key]>time.time():
                   continue
           except KeyError:
               pass
           debounce[key]=time.time()+0.1
           if verbose:
               print(event)
           if event.value==0:
               lirc_stop_repeat()
           elif event.type==ecodes.EV_KEY:
               try:
                   lirc_send(key_map[event.code])
               except KeyError:
                   pass
           elif event.type==ecodes.EV_ABS:
               debounce[key]=time.time()+0.5
               if event.code==0: # left joystick horiz
                   if event.value>5000:
                       lirc_send('fastforward')
                   elif event.value<-5000:
                       lirc_send('rewind')
               elif event.code==1: # left joystick vert
                   if event.value>5000:
                       lirc_send('stop')
                   elif event.value<-5000:
                       lirc_send('play')
               elif event.code==3: # right joystick horiz
                   if event.value>5000:
                       lirc_send('next')
                   elif event.value<-5000:
                       lirc_send('previous')
               elif event.code==4: # right joystick vert
                   debounce[key]=time.time()+0.5
                   if event.value<-3000:
                       lirc_send('zoom')
                   if event.value>3000:
                       lirc_send('audio')
               elif event.code==17: # left joypad vert
                   if event.value>0:
                       lirc_send('cursor_down')
                   if event.value<0:
                       lirc_send('cursor_up')
               elif event.code==16: # left joypad horiz
                   if event.value>0:
                       lirc_send('cursor_right')
                   if event.value<0:
                       lirc_send('cursor_left')
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
