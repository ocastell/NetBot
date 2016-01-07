#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# RaspBerry PI Wi-Fi Socket Server
# 2015 ocastell
#

import sys
import getopt
import os
import socket
import string
import pyroomba
from subprocess import Popen
from time import sleep
from time import time
from math import *

#
# Valors per defecte
#

VIDEO_PORT=8081
AUDIO_PORT=5500
SPEAK_PORT=5600
CLEAN_COMMAND = 135
SPOT_COMMAND = 134
DOCK_COMMAND = 143
SAFE_COMMAND = 131
TCP_PORT=9001
SOCKET_PORT=5
MAXDATA=1024
yemul=False
AUDIO_DEVICE='plughw:1,0' 
katamariTheme  =  [70, 72, 74, 75, 74, 70, 65, 70, 65, 68, 70, 68, 67, 65]
katamariTiming =  [32, 16, 16, 16, 16, 16, 32, 32, 32, 32, 16, 16, 32, 32]
sensors=[
         'bump_wheel_drops','cliff_left','cliff_front_left','cliff_front_right','cliff_right','virtual_wall','wheel_overcurrent','dirt_detect',
         'ir_character_omni','ir_character_left','ir_character_left','buttons','distance','angle','charging_state','voltage','current',
         'temperature','battery_charge','battery_capacity','wall_signal','cliff_left_signal','cliff_front_left_signal','cliff_front_right_signal',
         'cliff_right_signal','charging_sources_available','oi_mode','song_number','song_playing','stream_packets','requested_velocity',
         'requested_radius','requested_right_velocity','requested_left_velocity','right_encoder','left_encoder','light_bumper','light_bump_left',
         'light_bump_front_left','light_bump_center_left','light_bump_center_right','light_bump_front_right','left_motor_current',
         'right_motor_Current','main_brush_motor_current','side_brush_motor_current','stasis'
        ]          
sensors_group=[
         'ir_character_omni','ir_character_left','ir_character_right',
         'distance','angle',
         'charging_state','voltage','current',
         'temperature','battery_charge','battery_capacity',
         'right_encoder','left_encoder'
        ]          
#
# Fluxe principal del program
#
def main(argv):
    SERIAL_PORT=None
    serialport=None
    try:
       opts, args = getopt.getopt(argv,"hs:",["SERIAL_PORT="])
    except getopt.GetoptError:
       print 'python ./server__socket_netbot.py -s <serial_port> (/dev/null for emulate)'
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
          print 'python ./server__socket_netbot.py -s <serial_port> (/dev/null for emulate)'
          sys.exit()
       elif opt in ("-s", "--SERIAL_PORT"):
          SERIAL_PORT = arg
    if SERIAL_PORT == '/dev/null':
       serialport=SERIAL_PORT
       print 'Emulate serial port with ',SERIAL_PORT
       yemul=True
    else:
       try:
          roomba = pyroomba.Roomba(port=SERIAL_PORT, baud = 115200, timeout = 0.030, serial_port=serialport)
          roomba.start()
          roomba.safe()
          roomba.leds(255, 255)
          roomba.define_song(0, katamariTheme, katamariTiming)
          roomba.play_song(0)
          roomba.leds(0, 255)
          roomba.stream_samples( 
                                pyroomba.sensors.IR_CHARACTER_OMNI, pyroomba.sensors.IR_CHARACTER_LEFT, pyroomba.sensors.IR_CHARACTER_RIGHT, 
                                pyroomba.sensors.DISTANCE         , pyroomba.sensors.ANGLE            , pyroomba.sensors.CHARGING_STATE    ,
                                pyroomba.sensors.VOLTAGE          , pyroomba.sensors.CURRENT          , pyroomba.sensors.TEMPERATURE       , 
                                pyroomba.sensors.BATTERY_CHARGE   , pyroomba.sensors.BATTERY_CAPACITY , pyroomba.sensors.RIGHT_ENCODER     ,
                                pyroomba.sensors.LEFT_ENCODER
                               ) 
          print 'Connected to Roomba in port ',SERIAL_PORT
       except:
          print "Problem connecting with Roomba"
          exit()
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('', TCP_PORT))
    serversocket.listen(SOCKET_PORT)
    while 1:
       conn, addr = serversocket.accept()
       print 'The Server has Connected by Client ', addr
       host_ip=addr[0]
#
# Bucle per rebre les dades de la xarxa
#
       Bucle=True
       while Bucle:
#
# Intenta fer la lectura, si hi ha una interrupció per teclat (CRTL+C) s'atura, si hi ha alg�ún error (cau la connexió) també. 
#
          try:
             data = conn.recv(MAXDATA)
             #data = data.decode()
             data = data
             start=0
             end=data.find('*', start)
             data=data[start:end]
             data=data.strip()
             filter_data=filter(lambda x: x in string.printable, data)
             data=filter_data
             print len(data),data
#
# Si les dades rebudes són diferents a la benvinguda 'Hello' interpreta la comanda i l'envia al robot. 
#
             if (data <> 'Hello') & (len(data) > 0):
                list=data.split()
                code=int(list[0])
#
# Activa el servidor servidor perquè el robot parli el que s'escri. 
#
                if (code == SPEAK_PORT):   # Control the Speak Daemon (code+LAN+MSG)
                   lang=list[1]
                   #print "Language: ",lang
                   msg=list[2]
                   msg=msg.replace('_',' ')
                   msg='"'+msg+'"'
                   #print "message ",msg
                   commands=[]
                   command="echo "+msg+" | espeak -v "+lang+" > /dev/null 2> /dev/null &"
                   commands.append(command)
                   #print "commands ",commands
                   processes = [Popen(cmd, shell=True) for cmd in commands]
                   for p in processes: p.wait()
#
# Activa el servidor de so per poder escoltar al control remot el que escolta el robot
#
                elif (code == AUDIO_PORT):   # Control the Sound Stream Daemon with PulseAudio gst command
                   func=int(list[1])
                   if func == 1:      # 1 to start 0 to stop
                      commands=[]
                      command='gst-launch-1.0 -v alsasrc device='+AUDIO_DEVICE+' ! mulawenc ! rtppcmupay ! udpsink host='+host_ip+' port='+str(AUDIO_PORT)+' > /dev/null 2> /dev/null &'
                      commands.append(command)
                      processes = [Popen(cmd, shell=True) for cmd in commands]
                      for p in processes: p.wait()
                   elif func == 0:    # stop all the arecord & netcat process
                      commands=[]
                      command='killall gst-launch-1.0'
                      commands.append(command)
                      processes = [Popen(cmd, shell=True) for cmd in commands]
                      for p in processes: p.wait()
                elif (code == CLEAN_COMMAND):   # Send the clean command to robot
                      if(not yemul): roomba.clean()
                elif (code == SPOT_COMMAND):   # Send the spot command to robot
                      if(not yemul): roomba.spot()
                elif (code == DOCK_COMMAND):   # Send the dock command to robot
                      if(not yemul): roomba.dock()
                elif (code == SAFE_COMMAND):   # Send the safe command to robot
                      if(not yemul): roomba.start()
                      if(not yemul): roomba.safe()

#
# En un altre cas tenim una comanda de moviment o pròpia del robot.
#
                else:
                   speed=int(list[1])
                   radius=int(list[2])
                if (code == 145):    # Drive Direct (v_right, v_left)
                   right=speed
                   left=radius
                   if not serialport: 
                      if(not yemul): roomba.drive_direct(right,left) 
                elif (code == 137):  # Drive (v, radius)
                   if not serialport: 
                      if(not yemul): roomba.drive(speed,radius) 
#
# S'actualitza el poll dels sensors per enviar la info al sistema de control remot
#
             if (not yemul):
                dict=roomba.poll()
                sensor_char=''
                k=0
                for key in dict:
                    k=k+1
                    if k == 1:
                       sensor_char=key+' '+str(dict[key])
                    else:
                       sensor_char=sensor_char+' '+key+' '+str(dict[key])
                new_sensor_char=sensor_char
                if (len(sensor_char) < MAXDATA+1):
                   for i in range(0,MAXDATA-len(sensor_char)):
                       new_sensor_char=new_sensor_char+'*'
                else:
                   print "error: length of socket msg > MAXDATA"
                   exit()
                new_sensor_char=new_sensor_char.encode()
                conn.sendall(new_sensor_char)
          except KeyboardInterrupt:
             print 'Interrupted'
             try:
                 sys.exit(0)
             except SystemExit:
                 os._exit(0)
          except:
             print 'The Server has Disconnected by Client ', addr
             data=None
             conn=None
             Bucle=False
       if conn: conn.close()
    if roomba: roomba.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
