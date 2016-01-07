#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# NetBot Socket Remote Control and Stream Video & Audio GUI
# 2015 ocastell
#
# Import the Lybraries
#
import sys
import os
from subprocess import Popen
import shlex
import shutil
import socket
import pygtk
pygtk.require('2.0')
import gtk
import operator
import time
import string
import struct
import urllib
import gobject
import threading
#
# Initialize Values
#
# 1.- Roomba Values
#
CLEAN_COMMAND = 135
SPOT_COMMAND = 134
DOCK_COMMAND = 143
SAFE_COMMAND = 131
VELOCITYCHANGE = 200
ROTATIONCHANGE = 300
#
# 2.- Program Values
#
images='images'
MAXDATA=1024
#
# 3.- Classes
#

class NetBotGUI(object):
   window = gtk.Window(gtk.WINDOW_TOPLEVEL)
   button_Connection=gtk.Button()
   button_Disconnection=gtk.Button()
   button_Clean=gtk.Button()
   button_Spot=gtk.Button()
   button_Dock=gtk.Button()
   button_Refresh=gtk.Button()
   button_Video=gtk.Button()
   button_Audio=gtk.Button()
   button_Speak=gtk.Button()
   button_ArrowUp=gtk.Button()
   button_ArrowDown=gtk.Button()
   button_ArrowUpLeft=gtk.Button()
   button_ArrowUpRight=gtk.Button()
   button_ArrowDownLeft=gtk.Button()
   button_ArrowDownRight=gtk.Button()
   button_Stop=gtk.Button()
   button_SpinRight=gtk.Button()
   button_SpinLeft=gtk.Button()
   image_window=gtk.Image()
#
# Labels for display the sensors values
#
   lbl_conn=gtk.Label()
   lbl_battery=gtk.Label()
   lbl_voltage=gtk.Label()
   lbl_current=gtk.Label()
   lbl_temperature=gtk.Label()
   lbl_charging=gtk.Label()
   lbl_distance=gtk.Label()
   lbl_angle=gtk.Label()
   lbl_right_encoder=gtk.Label()
   lbl_left_encoder=gtk.Label()
   lbl_ir_left=gtk.Label()
   lbl_ir_right=gtk.Label()
   lbl_ir_omni=gtk.Label()
#
#
#
   TextIP=gtk.Entry()
   TextRobot=gtk.TextView()
   Language=gtk.combo_box_new_text()
   HText=gtk.HBox()
   fixed=gtk.Fixed()
   Battery=0
   audio_port="5500"
   video_port="8081"
   speak_port="5600"
   yaudio=False
   yvideo=False
   yclean=False
   yspot=False
   ydock=False
   WINDOW_WIDTH=600
   WINDOW_HEIGTH=500

   def ConnectWithNetBot(self, widget, data=None):
       self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.remote_ip = (self.TextIP.get_text())
       self.s.connect((self.remote_ip , self.port))
       self.STREAM_URL = 'http://'+self.remote_ip+':'+self.video_port+'/'
            
       self.RefreshNetBot(widget,None)

       widget.set_sensitive(False)
       self.button_Disconnection.set_sensitive(True)
       self.button_Clean.set_sensitive(True)
       self.button_Spot.set_sensitive(True)
       self.button_Dock.set_sensitive(True)
       self.button_Refresh.set_sensitive(True)
       self.button_Video.set_sensitive(True)
       self.button_Audio.set_sensitive(True)
       self.button_Speak.set_sensitive(True)
       self.button_ArrowUp.set_sensitive(True)
       self.button_ArrowDown.set_sensitive(True)
       self.button_ArrowUpLeft.set_sensitive(True)
       self.button_ArrowUpRight.set_sensitive(True)
       self.button_ArrowDownLeft.set_sensitive(True)
       self.button_ArrowDownRight.set_sensitive(True)
       self.button_Stop.set_sensitive(True)
       self.button_SpinRight.set_sensitive(True)
       self.button_SpinLeft.set_sensitive(True)
       self.TextRobot.set_sensitive(True)
       self.Language.set_sensitive(True)

#
# Update the sensors values from Robot
#
   def RefreshNetBot(self,widget,data=None):
        try:
           time.sleep(2)
           self.sendCommandASCII(str(SAFE_COMMAND)) 
	   self.sendCommandASCII('Hello')
           time.sleep(2)
        except:
            mytext="CAN'T CONNECT"
            self.lbl_conn.set_markup('<span foreground="black" size="medium"><b>Status: </b></span><span color="darkgreen"><i>'+mytext+'</i></span>')
            return
        yemul=False
        if (not yemul):
	    data = self.s.recv(MAXDATA)
            data=data.decode()
            start=0
            end=data.find('*', start)
            data=data[start:end]
            data_list=data.split()
            print data_list

            mytext='Connected'
            self.lbl_conn.set_markup('<span foreground="black" size="medium"><b>Status: </b></span><span color="darkgreen"><i>'+mytext+'</i></span>')
            
            index=data_list.index('battery_charge')
            charge=int(data_list[index+1])
            index=data_list.index('battery_capacity')
            capacity=int(data_list[index+1])
            per_cent=100*float(charge)/float(capacity)
            mytext="{:.2f}".format(per_cent)
            self.lbl_battery.set_markup('<span foreground="black" size="medium"><b>Battery: </b></span><span color="darkblue"><i>'+mytext+' %</i></span>')
    
            index=data_list.index('voltage')
            voltage=int(data_list[index+1])
            mytext=str(voltage)
            self.lbl_voltage.set_markup('<span foreground="black" size="medium"><b>Voltage: </b></span><span color="darkblue"><i>'+mytext+' mV</i></span>')
    
            index=data_list.index('current')
            current=int(data_list[index+1])
            mytext=str(current)
            self.lbl_current.set_markup('<span foreground="black" size="medium"><b>Current: </b></span><span color="darkblue"><i>'+mytext+' mA</i></span>')
    
            index=data_list.index('temperature')
            temperature=int(data_list[index+1])
            mytext=str(temperature)
            self.lbl_temperature.set_markup('<span foreground="black" size="medium"><b>Temperature: </b></span><span color="darkblue"><i>'+mytext+' Celsius</i></span>')
    
            index=data_list.index('charging_state')
            charging=int(data_list[index+1])
            if charging == 0:
               mytext='Not Charging'
            elif charging == 1:
               mytext='Reconditioning Charging'
            elif charging == 2:
               mytext='Full Charging'
            elif charging == 3:
               mytext='Trickle Charging'
            elif charging == 4:
               mytext='Waiting'
            elif charging == 5:
               mytext='Charging Fault Condition'
            self.lbl_charging.set_markup('<span foreground="black" size="medium"><b>Charging State: </b></span><span color="darkblue"><i>'+mytext+'</i></span>')
    
            index=data_list.index('distance')
            distance=int(data_list[index+1])*1000
            mytext=str(distance)
            self.lbl_distance.set_markup('<span foreground="black" size="medium"><b>Distance: </b></span><span color="darkblue"><i>'+mytext+' m</i></span>')
    
            index=data_list.index('angle')
            angle=float(int(data_list[index+1]))%360.
            mytext=str(angle)
            self.lbl_angle.set_markup('<span foreground="black" size="medium"><b>Angle: </b></span><span color="darkblue"><i>'+mytext+' Degrees</i></span>')
    
            index=data_list.index('right_encoder')
            right_encoder=int(data_list[index+1])
            mytext=str(right_encoder)
            self.lbl_right_encoder.set_markup('<span foreground="black" size="medium"><b>Right encoder: </b></span><span color="darkblue"><i>'+mytext+' Encoder</i></span>')

            index=data_list.index('left_encoder')
            left_encoder=int(data_list[index+1])
            mytext=str(left_encoder)
            self.lbl_left_encoder.set_markup('<span foreground="black" size="medium"><b>Left encoder: </b></span><span color="darkblue"><i>'+mytext+' Encoder</i></span>')

            index=data_list.index('ir_character_omni')
            ir_character_omni=int(data_list[index+1])
            mytext=str(ir_character_omni)
            self.lbl_ir_omni.set_markup('<span foreground="black" size="medium"><b>IR Omni: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')

            #index=data_list.index('ir_character_right')
            #ir_character_right=int(data_list[index+1])
            mytext='0'
            self.lbl_ir_right.set_markup('<span foreground="black" size="medium"><b>IR Right: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')

            index=data_list.index('ir_character_left')
            ir_character_left=int(data_list[index+1])
            mytext=str(ir_character_left)
            self.lbl_ir_left.set_markup('<span foreground="black" size="medium"><b>IR Left: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')
        else:
             print "Not sensors data, perhaps EMUL?"
        return

   def CleanNetBot(self, widget,  data=None):
       if self.yclean:
	  imageClean= gtk.Image()
          imagename=images+"/Clean.png"
	  imageClean.set_from_file(imagename)
	  self.button_Clean.set_image(imageClean)
	  self.button_Clean.set_tooltip_text("Stop Clean Mode Button")
          self.sendCommandASCII(str(SAFE_COMMAND)) 
          self.yclean=False
       else:
	  imageClean= gtk.Image()
          imagename=images+"/CleanStop.png"
	  imageClean.set_from_file(imagename)
	  self.button_Clean.set_image(imageClean)
	  self.button_Clean.set_tooltip_text("Start Clean Mode Button")
	  self.sendCommandASCII(str(CLEAN_COMMAND))
          self.yclean=True

   def SpotNetBot(self, widget,  data=None):
       if self.yspot:
	  imageSpot= gtk.Image()
          imagename=images+"/Spot.png"
	  imageSpot.set_from_file(imagename)
	  self.button_Spot.set_image(imageSpot)
	  self.button_Spot.set_tooltip_text("Stop Spot Mode Button")
          self.sendCommandASCII(str(SAFE_COMMAND)) 
          self.yspot=False
       else:
	  imageSpot= gtk.Image()
          imagename=images+"/SpotStop.png"
	  imageSpot.set_from_file(imagename)
	  self.button_Spot.set_image(imageSpot)
	  self.button_Spot.set_tooltip_text("Start Spot Mode Button")
	  self.sendCommandASCII(str(SPOT_COMMAND))
          self.yspot=True

   def DockNetBot(self, widget,  data=None):
       if self.ydock:
	  imageDock= gtk.Image()
          imagename=images+"/Dock.png"
	  imageDock.set_from_file(imagename)
	  self.button_Dock.set_image(imageDock)
	  self.button_Dock.set_tooltip_text("Stop Dock Mode Button")
          self.sendCommandASCII(str(SAFE_COMMAND)) 
          self.ydock=False
       else:
	  imageDock= gtk.Image()
          imagename=images+"/DockStop.png"
	  imageDock.set_from_file(imagename)
	  self.button_Dock.set_image(imageDock)
	  self.button_Dock.set_tooltip_text("Start Dock Mode Button")
	  self.sendCommandASCII(str(DOCK_COMMAND))
          self.ydock=True

   def DisconnectWithNetBot(self, widget,  data=None):
        msg="Bye, bye ..."
        self.sendCommandASCII(str(msg)) 
	widget.set_sensitive(False)
	self.button_Connection.set_sensitive(True)
	self.button_Clean.set_sensitive(False)
	self.button_Spot.set_sensitive(False)
	self.button_Dock.set_sensitive(False)
	self.button_Refresh.set_sensitive(False)
	self.button_Video.set_sensitive(False)
	self.button_Audio.set_sensitive(False)
	self.button_Speak.set_sensitive(False)
	self.button_ArrowUp.set_sensitive(False)
	self.button_ArrowDown.set_sensitive(False)
	self.button_ArrowUpLeft.set_sensitive(False)
	self.button_ArrowUpRight.set_sensitive(False)
	self.button_ArrowDownLeft.set_sensitive(False)
	self.button_ArrowDownRight.set_sensitive(False)
	self.button_Stop.set_sensitive(False)
	self.button_SpinRight.set_sensitive(False)
	self.button_SpinLeft.set_sensitive(False)
	self.TextRobot.set_sensitive(False)
	self.Language.set_sensitive(False)
        self.Stop_Video_Process()
        self.Stop_Audio_Process()
	self.s.close()

   def delete_event(self, widget, event, data=None):
	if self.s : self.s.close()
        self.Stop_Video_Audio_Process()
	return False

   def destroy(self, widget, data=None):
        self.Stop_Video_Audio_Process()
        gobject.idle_add(quit)
	if self.s : self.s.close()
	gtk.main_quit()

   def About_clicked(self, widget, data=None):
        about = gtk.AboutDialog()
        about.set_program_name("NetBot Socket Remote Control")
        about.set_version("1.0")
        about.set_copyright("O. Castell (2015)")
        about.set_comments("NetBot Python Remote Management Software")
        about.set_website("http://www.iesdeltebre.net")
        imagename=images+"/NetBot.png"
        about.set_logo(gtk.gdk.pixbuf_new_from_file(imagename))
        about.run()
        about.destroy()

   def MoveUpNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity += VELOCITYCHANGE
        self.rotation = 0
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def MoveDownNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity -= VELOCITYCHANGE
        self.rotation = 0
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def MoveUpRightNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity += VELOCITYCHANGE
        self.rotation = 0
        self.rotation -= ROTATIONCHANGE/2
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def MoveUpLeftNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity += VELOCITYCHANGE
        self.rotation = 0
        self.rotation += ROTATIONCHANGE/2
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def MoveDownRightNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity -= VELOCITYCHANGE
        self.rotation = 0
        self.rotation += ROTATIONCHANGE/2
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def MoveDownLeftNetBot(self, widget,  data=None):
        self.velocity = 0
        self.velocity -= VELOCITYCHANGE
        self.rotation = 0
        self.rotation -= ROTATIONCHANGE/2
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def SpinLeftNetBot(self, widget,  data=None):
        self.velocity = 0
        self.rotation = 0
        self.rotation += ROTATIONCHANGE
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def SpinRightNetBot(self, widget,  data=None):
        self.velocity = 0
        self.rotation = 0
        self.rotation -= ROTATIONCHANGE
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def StopNetBot(self, widget,  data=None):
        self.velocity = 0
        self.rotation = 0
        self.Velocity()
        cmd_str="145"+" "+str(self.vr)+" "+str(self.vl)
        self.sendCommandASCII(cmd_str)

   def Velocity(self):
        self.vr = self.velocity + (self.rotation/2)
        self.vl = self.velocity - (self.rotation/2)
        return

   def VideoFromNetBot(self, widget,  data=None):
       if self.yvideo:
	  imageVideo= gtk.Image()
          imagename=images+"/Video.png"
	  imageVideo.set_from_file(imagename)
	  self.button_Video.set_image(imageVideo)
	  self.button_Video.set_tooltip_text("Start Video Streaming Button")
          self.Stop_Video_Process()
       else:
	  imageVideo= gtk.Image()
          imagename=images+"/VideoStop.png"
	  imageVideo.set_from_file(imagename)
	  self.button_Video.set_image(imageVideo)
	  self.button_Video.set_tooltip_text("Stop Video Streaming Button")
          gobject.threads_init()
          self.t = VideoThread(self.image_window,self.STREAM_URL)
          self.t.start()
          self.yvideo=True

   def AudioFromNetBot(self, widget,  data=None):
       if self.yaudio:
	  imageAudio= gtk.Image()
          imagename=images+"/Audio.png"
	  imageAudio.set_from_file(imagename)
	  self.button_Audio.set_image(imageAudio)
	  self.button_Audio.set_tooltip_text("Start Audio Streaming Button")
          self.Stop_Audio_Process()
       else:
	  imageAudio= gtk.Image()
          imagename=images+"/AudioStop.png"
	  imageAudio.set_from_file(imagename)
	  self.button_Audio.set_image(imageAudio)
	  self.button_Audio.set_tooltip_text("Stop Audio Streaming Button")
          cmd_str=self.audio_port+" 1"
          self.sendCommandASCII(cmd_str)
          time.sleep(1)
          commands=[]
          command='gst-launch-1.0 -v udpsrc port='+self.audio_port+' caps="application/x-rtp" ! queue ! rtppcmudepay ! mulawdec ! audioconvert ! autoaudiosink sync=false > /dev/null 2> /dev/null  &'
          commands.append(command)
          self.processes = [Popen(cmd, shell=True) for cmd in commands]
          self.yaudio=True

   def SpeaktoNetBot(self, widget,  data=None):
          model = self.Language.get_model()
          index = self.Language.get_active()
          idioma=[' ','en','ca','es']
          lang=idioma[index] 
          startiter, enditer = self.buffer.get_bounds()
          msg=self.buffer.get_text(startiter, enditer)
          msg=msg.replace(' ','_')
          cmd_str=self.speak_port+" "+lang+" "+msg
          self.sendCommandASCII(cmd_str)
          time.sleep(1)
  
   def Stop_Video_Process(self):
       if self.yvideo:
          self.t.quit=True
          self.t.join()
          self.yvideo=False

   def Stop_Audio_Process(self):
       if self.yaudio:
          cmd_str=self.audio_port+" 0"
          self.sendCommandASCII(cmd_str)
          time.sleep(1)
          self.yaudio=False
          commands=[]
          command="killall gst-launch-1.0"
          commands.append(command)
          self.processes = [Popen(cmd, shell=True) for cmd in commands]
          for p in self.processes: p.wait()

   def Stop_Video_Audio_Process(self):
       if self.yvideo:
          self.Stop_Video_Process()
       if self.yaudio:
          self.Stop_Audio_Process()
       return

   def sendCommandASCII(self, command):
        new_command=command
        if (len(command) < MAXDATA+1):
           for i in range(0,MAXDATA-len(command)):
               new_command=new_command+'*'
        else:       
           print "error: length of socket msg > MAXDATA"
           exit()
        new_command=new_command.encode()
        self.s.sendall(new_command)

   def __init__(self):
	self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.remote_ip = '192.168.1.12'
	self.port = 9001

	self.window.set_title("NetBot Socket Remote Control")
	self.window.set_size_request(self.WINDOW_WIDTH,self.WINDOW_HEIGTH)
	self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(35500, 35000, 38000))
	self.window.set_position(gtk.WIN_POS_CENTER)
	self.window.set_resizable(True)

	self.window.connect("delete_event", self.delete_event)
	self.window.connect("destroy", lambda w: gtk.main_quit())
	self.window.set_border_width(10)

	self.button_Clean.set_sensitive(False)
	self.button_Spot.set_sensitive(False)
	self.button_Dock.set_sensitive(False)
	self.button_Disconnection.set_sensitive(False)
	self.button_Refresh.set_sensitive(False)
	self.button_Video.set_sensitive(False)
	self.button_Audio.set_sensitive(False)
	self.button_Speak.set_sensitive(False)
	self.button_ArrowUp.set_sensitive(False)
	self.button_ArrowDown.set_sensitive(False)
	self.button_ArrowUpLeft.set_sensitive(False)
	self.button_ArrowUpRight.set_sensitive(False)
	self.button_ArrowDownLeft.set_sensitive(False)
	self.button_ArrowDownRight.set_sensitive(False)
	self.button_Stop.set_sensitive(False)
	self.button_SpinRight.set_sensitive(False)
	self.button_SpinLeft.set_sensitive(False)
	self.TextRobot.set_sensitive(False)
	self.Language.set_sensitive(False)

	self.TextIP.set_text("NetBot IP Address")
	self.TextIP.set_width_chars(15)
	self.TextIP.set_size_request(155,32)

	self.TextRobot.set_sensitive(False)
        self.buffer=self.TextRobot.get_buffer()
	self.buffer.set_text("This is some text that Netbot can speak ... ")

	self.Language.set_sensitive(False)
        self.Language.append_text('Select a Language:')
        self.Language.append_text('English')
        self.Language.append_text('Català')
        self.Language.append_text('Español')
        self.Language.set_active(1)

	imageCon = gtk.Image()
        imagename=images+"/stock_connect_24.png"
	imageCon.set_from_file(imagename)
	self.button_Connection.set_image(imageCon)
	self.button_Connection.set_tooltip_text("Connect NetBot Remote Socket")
	self.button_Connection.connect("clicked", self.ConnectWithNetBot, None)

	imageDiscon = gtk.Image()
        imagename=images+"/stock_disconnect_24.png"
	imageDiscon.set_from_file(imagename)
	self.button_Disconnection.set_image(imageDiscon)
	self.button_Disconnection.set_tooltip_text("Disconnect NetBot Remote Socket")
	self.button_Disconnection.connect("clicked", self.DisconnectWithNetBot, None)

	imageRefresh= gtk.Image()
        imagename=images+"/stock_refresh_24.png"
	imageRefresh.set_from_file(imagename)
	self.button_Refresh.set_image(imageRefresh)
	self.button_Refresh.set_tooltip_text("Refresh Battery State")
	self.button_Refresh.connect("clicked", self.RefreshNetBot, None)

	imageAbout = gtk.Image()
        imagename=images+"/stock_info_24.png"
	imageAbout.set_from_file(imagename)
	self.button_About=gtk.Button()
	self.button_About.set_image(imageAbout)
	self.button_About.set_tooltip_text("About NetBot Socket Remote Control")
	self.button_About.connect("clicked", self.About_clicked, None)

	imageClean= gtk.Image()
        imagename=images+"/Clean.png"
	imageClean.set_from_file(imagename)
	self.button_Clean.set_image(imageClean)
	self.button_Clean.set_tooltip_text("Clean Button")
	self.button_Clean.connect("clicked", self.CleanNetBot, None)

	imageSpot= gtk.Image()
        imagename=images+"/Spot.png"
	imageSpot.set_from_file(imagename)
	self.button_Spot.set_image(imageSpot)
	self.button_Spot.set_tooltip_text("Spot Button")
	self.button_Spot.connect("clicked", self.SpotNetBot, None)

	imageDock= gtk.Image()
        imagename=images+"/Dock.png"
	imageDock.set_from_file(imagename)
	self.button_Dock.set_image(imageDock)
	self.button_Dock.set_tooltip_text("Dock Button")
	self.button_Dock.connect("clicked", self.DockNetBot, None)

	imageUpRight= gtk.Image()
        imagename=images+"/ArrowRightUp.png"
	imageUpRight.set_from_file(imagename)
	self.button_ArrowUpRight.set_image(imageUpRight)
	self.button_ArrowUpRight.set_tooltip_text("Move Front & Right Button")
	self.button_ArrowUpRight.connect("clicked", self.MoveUpRightNetBot, None)

	imageUpLeft= gtk.Image()
        imagename=images+"/ArrowLeftUp.png"
	imageUpLeft.set_from_file(imagename)
	self.button_ArrowUpLeft.set_image(imageUpLeft)
	self.button_ArrowUpLeft.set_tooltip_text("Move Front & Left Button")
	self.button_ArrowUpLeft.connect("clicked", self.MoveUpLeftNetBot, None)

	imageDownRight= gtk.Image()
        imagename=images+"/ArrowRightDown.png"
	imageDownRight.set_from_file(imagename)
	self.button_ArrowDownRight.set_image(imageDownRight)
	self.button_ArrowDownRight.set_tooltip_text("Move Rear & Right Button")
	self.button_ArrowDownRight.connect("clicked", self.MoveDownRightNetBot, None)

	imageDownLeft= gtk.Image()
        imagename=images+"/ArrowLeftDown.png"
	imageDownLeft.set_from_file(imagename)
	self.button_ArrowDownLeft.set_image(imageDownLeft)
	self.button_ArrowDownLeft.set_tooltip_text("Move Rear & Left Button")
	self.button_ArrowDownLeft.connect("clicked", self.MoveDownLeftNetBot, None)

	imageUp= gtk.Image()
        imagename=images+"/ArrowUp.png"
	imageUp.set_from_file(imagename)
	self.button_ArrowUp.set_image(imageUp)
	self.button_ArrowUp.set_tooltip_text("Move Front Button")
	self.button_ArrowUp.connect("clicked", self.MoveUpNetBot, None)

	imageDown= gtk.Image()
        imagename=images+"/ArrowDown.png"
	imageDown.set_from_file(imagename)
	self.button_ArrowDown.set_image(imageDown)
	self.button_ArrowDown.set_tooltip_text("Move Back Button")
	self.button_ArrowDown.connect("clicked", self.MoveDownNetBot, None)

	imageStop= gtk.Image()
        imagename=images+"/Stop.png"
	imageStop.set_from_file(imagename)
	self.button_Stop.set_image(imageStop)
	self.button_Stop.set_tooltip_text("Stop Button")
	self.button_Stop.connect("clicked", self.StopNetBot, None)

	imageSpinLeft= gtk.Image()
        imagename=images+"/ArrowSpinLeft.png"
	imageSpinLeft.set_from_file(imagename)
	self.button_SpinLeft.set_image(imageSpinLeft)
	self.button_SpinLeft.set_tooltip_text("Turn Left Button")
	self.button_SpinLeft.connect("clicked", self.SpinLeftNetBot, None)

	imageSpinRight= gtk.Image()
        imagename=images+"/ArrowSpinRight.png"
	imageSpinRight.set_from_file(imagename)
	self.button_SpinRight.set_image(imageSpinRight)
	self.button_SpinRight.set_tooltip_text("Turn Right Button")
	self.button_SpinRight.connect("clicked", self.SpinRightNetBot, None)

	imageAudio= gtk.Image()
        imagename=images+"/Audio.png"
	imageAudio.set_from_file(imagename)
	self.button_Audio.set_image(imageAudio)
	self.button_Audio.set_tooltip_text("Start Audio Streaming Button")
	self.button_Audio.connect("clicked", self.AudioFromNetBot, None)

	imageSpeak= gtk.Image()
        imagename=images+"/Speak.png"
	imageSpeak.set_from_file(imagename)
	self.button_Speak.set_image(imageSpeak)
	self.button_Speak.set_tooltip_text("Send Text to NetBot speaker")
	self.button_Speak.connect("clicked", self.SpeaktoNetBot, None)

	imageVideo= gtk.Image()
        imagename=images+"/Video.png"
	imageVideo.set_from_file(imagename)
	self.button_Video.set_image(imageVideo)
	self.button_Video.set_tooltip_text("Start Video Streaming Button")
	self.button_Video.connect("clicked", self.VideoFromNetBot, None)

	#self.label.set_label("Battery: xxx%")

	imageHSeparator = gtk.Image()
        imagename=images+"/HSeparator.png"
	imageHSeparator.set_from_file(imagename)
	self.button_HSeparator=gtk.Button()
	self.button_HSeparator.set_size_request(400,1)
	self.button_HSeparator.set_image(imageHSeparator)

	imageVSeparator = gtk.Image()
        imagename=images+"/VSeparator.png"
	imageVSeparator.set_from_file(imagename)
	self.button_VSeparator=gtk.Button()
	self.button_VSeparator.set_size_request(1,600)
	self.button_VSeparator.set_image(imageVSeparator)

        self.image_window.set_size_request(320, 240)
        imagename=images+"/VideoOff.png"
	self.image_window.set_from_file(imagename)

	self.fixed.put(self.button_Connection,165,10)
	self.fixed.put(self.button_Disconnection,205,10)
	self.fixed.put(self.button_Refresh,245,10)
	self.fixed.put(self.button_About,285,10)

	self.fixed.put(self.button_Clean,390,5)
	self.fixed.put(self.button_Spot,440,5)
	self.fixed.put(self.button_Dock,490,5)

	self.fixed.put(self.button_HSeparator,-15,65)
	self.fixed.put(self.button_VSeparator,345,-10)

	self.fixed.put(self.image_window,5,80)
	self.fixed.put(self.button_Video,5,325)
	self.fixed.put(self.button_Audio,65,325)
	self.fixed.put(self.button_Speak,275,325)
	self.fixed.put(self.Language,125,325)
	self.fixed.put(self.TextIP,5,10)
        self.HText.set_size_request(325,75)
	self.fixed.put(self.HText,5,400)
        self.TextRobot.set_wrap_mode(gtk.WRAP_CHAR)
	self.HText.add(self.TextRobot)

	self.fixed.put(self.button_Stop,440,150)
	self.fixed.put(self.button_ArrowUpRight,500,90)
	self.fixed.put(self.button_ArrowUpLeft,380,90)
	self.fixed.put(self.button_ArrowDownRight,500,210)
	self.fixed.put(self.button_ArrowDownLeft,380,210)
	self.fixed.put(self.button_ArrowUp,440,90)
	self.fixed.put(self.button_ArrowDown,440,210)
	self.fixed.put(self.button_SpinRight,500,150)
	self.fixed.put(self.button_SpinLeft,380,150)

        mytext='Not Connected'
        self.lbl_conn.set_markup('<span foreground="black" size="medium"><b>Status: </b></span><span color="darkred"><i>'+mytext+'</i></span>')
        mytext='0'
        self.lbl_battery.set_markup('<span foreground="black" size="medium"><b>Battery: </b></span><span color="darkblue"><i>'+mytext+' %</i></span>')
        mytext='0'
        self.lbl_voltage.set_markup('<span foreground="black" size="medium"><b>Voltage: </b></span><span color="darkblue"><i>'+mytext+' V</i></span>')
        mytext='0'
        self.lbl_current.set_markup('<span foreground="black" size="medium"><b>Current: </b></span><span color="darkblue"><i>'+mytext+' A</i></span>')
        mytext='0'
        self.lbl_temperature.set_markup('<span foreground="black" size="medium"><b>Temperature: </b></span><span color="darkblue"><i>'+mytext+' Celsius</i></span>')
        mytext='Off'
        self.lbl_charging.set_markup('<span foreground="black" size="medium"><b>Charging State: </b></span><span color="darkblue"><i>'+mytext+'</i></span>')
        mytext='0'
        self.lbl_distance.set_markup('<span foreground="black" size="medium"><b>Distance: </b></span><span color="darkblue"><i>'+mytext+' m</i></span>')
        mytext='0'
        self.lbl_angle.set_markup('<span foreground="black" size="medium"><b>Angle: </b></span><span color="darkblue"><i>'+mytext+' Degrees</i></span>')
        mytext='0'
        self.lbl_right_encoder.set_markup('<span foreground="black" size="medium"><b>Right encoder: </b></span><span color="darkblue"><i>'+mytext+' Encoder</i></span>')
        mytext='0'
        self.lbl_left_encoder.set_markup('<span foreground="black" size="medium"><b>Left encoder: </b></span><span color="darkblue"><i>'+mytext+' Encoder</i></span>')
        mytext='0'
        self.lbl_ir_omni.set_markup('<span foreground="black" size="medium"><b>IR Omni: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')
        mytext='0'
        self.lbl_ir_right.set_markup('<span foreground="black" size="medium"><b>IR Right: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')
        mytext='0'
        self.lbl_ir_left.set_markup('<span foreground="black" size="medium"><b>IR Left: </b></span><span color="darkblue"><i>'+mytext+' IR</i></span>')

	self.fixed.put(self.lbl_conn,380,275)
	self.fixed.put(self.lbl_battery,380,290)
	self.fixed.put(self.lbl_voltage,380,305)
	self.fixed.put(self.lbl_current,380,320)
	self.fixed.put(self.lbl_temperature,380,335)
	self.fixed.put(self.lbl_charging,380,350)
	self.fixed.put(self.lbl_distance,380,365)
	self.fixed.put(self.lbl_angle,380,380)
	self.fixed.put(self.lbl_right_encoder,380,395)
	self.fixed.put(self.lbl_left_encoder,380,410)
	self.fixed.put(self.lbl_ir_right,380,425)
	self.fixed.put(self.lbl_ir_left,380,440)
	self.fixed.put(self.lbl_ir_omni,380,455)

	self.window.add(self.fixed)
	self.window.show_all()

class VideoThread(threading.Thread):
    '''
    A background thread that takes the MJPEG stream and
    updates the GTK image.
    '''
    def __init__(self, widget,STREAM_URL='http://8.8.8.8:8081'):
        super(VideoThread, self).__init__()
        self.widget = widget
        self.quit = False
        #print 'connecting to', STREAM_URL
        self.stream = urllib.urlopen(STREAM_URL)

    def get_raw_frame(self):
        '''
        Parse an MJPEG http stream and yield each frame.
        Source: http://stackoverflow.com/a/21844162
        :return: generator of JPEG images
        '''
        raw_buffer = ''
        while True:
            new = self.stream.read(5034)
            if not new:
                # Connection dropped
                yield None
            raw_buffer += new
            a = raw_buffer.find('\xff\xd8')
            b = raw_buffer.find('\xff\xd9')
            if a != -1 and b != -1:
                frame = raw_buffer[a:b+2]
                raw_buffer = raw_buffer[b+2:]
                yield frame

    def run(self):
        for frame in self.get_raw_frame():
            if self.quit or frame is None:
                return
            loader = gtk.gdk.PixbufLoader('jpeg')
            loader.write(frame)
            loader.close()
            pixbuf = loader.get_pixbuf()
            # Schedule image update to happen in main thread
            gobject.idle_add(self.widget.set_from_pixbuf, pixbuf)
#
# Fluxe principal del program
#
def main(argv):
    controller = NetBotGUI()
    gtk.main()
    gobject.idle_add(quit)

if __name__ == '__main__':
     main(sys.argv[1:])
