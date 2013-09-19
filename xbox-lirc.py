from evdev import InputDevice, ecodes
from select import select
import subprocess, time

#EV_ABS 3
#EV_CNT 32
#EV_FF 21
#EV_FF_STATUS 23
#EV_KEY 1
#EV_LED 17
#EV_MAX 31
#EV_MSC 4
#EV_PWR 22
#EV_REL 2
#EV_REP 20
#EV_SND 18
#EV_SW 5
#EV_SYN 0

key_map = {
           304:'ok', # green button
           305:'back', # red button
           307:'menu', # blue button
           308:'escape', # yellow button
           310:'channel_down', # left button
           311:'channel_up', # right button
           312:'volume_down', # left trigger
           313:'volume_up', # right trigger
           314:'subtitle', # back
           315:'record', # start button
           316:'power', # xbox button
           317:'pause', # push down on left joystick
           318:'info', # push down on right joystick
}

repeating_commands = {
    'volume_up':True,
    'volume_down':True
}

repeat_cmd = None

def lirc_send(cmd, start=False, stop=False):
    global repeat_cmd
    if stop==False and repeat_cmd is not None:
        lirc_send(repeat_cmd,stop=True)
    t = "send_once"
    if start==True or (stop==False and repeating_commands.has_key(cmd)):
        t = "send_start"
        repeat_cmd=cmd
    elif stop==True:
        t = "send_stop"
        repeat_cmd=None
    print(' '.join([str(time.time()), "/usr/bin/irsend",t,"humax",cmd]))
    subprocess.call(["/usr/bin/irsend",t,"humax",cmd])
    
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
       print(event)
       if event.value==0:
           if repeat_cmd is not None:
               lirc_send(repeat_cmd,stop=True)
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
