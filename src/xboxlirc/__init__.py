"""Module/script to act as a bridge between an Xbox360 controller and LIRC"""

import subprocess, time
from target import TARGET

__all__ = ['verbose', 'key_map', 'repeating_commands', 'lirc_send', 'lirc_stop_repeat']

verbose=False

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
    """send a LIRC command to the configured device"""
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
    if verbose:
       print(' '.join([str(time.time()), "/usr/bin/irsend",t,TARGET,cmd]))
    subprocess.call(["/usr/bin/irsend",t,TARGET,cmd])

def lirc_stop_repeat():
    """stops a repeating command (if one if currently active)"""
    global repeat_cmd
    if repeat_cmd is not None:
        lirc_send(repeat_cmd,stop=True)
