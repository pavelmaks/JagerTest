#pavel molodec

import gi
import os
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf, GLib
from gi.repository import Gdk, Gst

import Jager2 as j
import cv2
import numpy as np
import threading
import time
import RPi.GPIO as GPIO
import configparser
#import VideoPlayer as vp



Gst.init(None)
Gst.init_check(None)

class InstructionBox(Gtk.Box):

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        self.servo = None

        self.parent = parent

        self.led = j.LED()

        self.busy = False
        self.target="./video/v2.mp4"
        self.cap = cv2.VideoCapture(self.target)
        self.ret, self.frame = self.cap.read()
        self.stack = Gtk.Overlay()
        self.add(self.stack)
        background = Gtk.Image.new_from_file('./video/photo2.png')
        self.stack.add(background)
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('./video/photo2.png', 480, 800)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)


        self.setStatusText(0)
        button = Gtk.Button(label='Установите емкость и нажмите')
        button.set_property("opacity", 0)
        button.connect("clicked", self.servoGo)

        self.stack.add_overlay(button)

    def onOpen(self):
        print('Instruction open')
        print(12)
        #self.servo.start()
        time.sleep(0.1)
        print(13)
        self.led.on()
        print(14)
        self.setStatusText(0)
        print(15)
        self.busy = False
        print(16)
        self.show_all()
        self.grab_focus()
        self.update = True
        print(111)
        threading.Thread(target=self.startPreview, args=()).start()

        print(17)

    def startPreview(self):
        while self.update:
            GLib.idle_add(self.showFrame)
            time.sleep(0.07)

    def showFrame(self):  # демонстрация кадра на экран

        # print('tick')

        if (self.ret == False):
            self.cap.release()
            self.cap = cv2.VideoCapture(self.target)
            self.ret, self.frame = self.cap.read()
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2] * frame.shape[1])
        self.image_renderer.set_from_pixbuf(pb.copy())
        self.ret, self.frame = self.cap.read()


    def onClose(self):
        #self.servo.close()
        self.update = False
        self.cap.release()
        print('Instruction close')

    def setStatusText(self, num):#изменение фона и надписей
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.target="./video/v2.mp4"
            self.ret = False
        elif num == 1:
            self.target = "./video/v3.mp4"
            self.ret = False
        elif num == 2:
            self.target = "./video/v4.mp4"
            self.ret = False

    def setBackground(self, num):#изменение фона
        if num == 0:
            self.background.set_from_file("disp_start.png")
        elif num == 1:
            self.background.set_from_file("disp_fill.png")
        elif num == 2:
            self.background.set_from_file("disp_finish.png")
        #self.background.show()

    def toIdle(self):
        self.parent.openBox(self, 0)
        self.led.off()
        self.update = False
        self.cap.release()
        print("toIdle")


    def servoGo(self, widget):#запуск процесса розлива
        print(18)
        if self.busy:
            return
        print(19)
        self.setStatusText(1)
        print(20)
        self.busy = True
        print(21)
        threading.Thread(target=self.servoAct, args=()).start()

    def servoAct(self):#запуск налива и возвращение в первую форму
        print(22)
        servoTime=j.get_setting(j.path, 'Settings', 'servoTime')
        print(23)
        servo = j.ServoAct()
        print(24)
        print('servoGo')
        servo.setActPosition()
        print(25)
        time.sleep(0.4)
        print(26)
        print('servoOnPlace')
        #self.servo.hold()
        time.sleep(servoTime)

        print('servoGoHome')
        servo.setIdlePosition()
        time.sleep(0.4)

        print('servoEnd')
        servo.hold()
        time.sleep(1)

        self.setStatusText(2)

        time.sleep(10)

        self.toIdle()

    def close(self):
        self.servo.close()
        print('close instr')

class IdleBox(Gtk.Box):#стартовая форма

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        self.parent = parent
        self.file = "./video/v1.mp4"
        self.cap = cv2.VideoCapture(self.file)
        self.ret, self.frame = self.cap.read()
        self.stack = Gtk.Overlay()
        self.add(self.stack)
        background = Gtk.Image.new_from_file('./video/photo1.png')
        self.stack.add(background)


        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('./video/photo1.png', 480, 800)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)
        self.update = False

        #player = OneMorePlayer()
        #overlay.add_overlay(player)

        #self.videoWidget = GstWidget('file:///home/pi/Documents/video')
        #self.videoWidget.set_size_request(480, 800)

        #self.gstPlayer = GstPlayer()
        #self.gstPlayer.setup_player('video.mkv')
        #self.gstPlayer.play()

        #overlay.add_overlay(self.gstPlayer)

        button = Gtk.Button(label='Нажмите, чтобы начать')
        button.set_property("opacity", 0)
        button.connect("clicked", self.toScanner) # привязка тригера на переход к qr коду

        self.stack.add_overlay(button)

        """
        exitbutton = Gtk.Button(label='X')
        #exitbutton.set_property('opacity', 0)
        exitbutton.connect("clicked", parent.destroy)
        exitbutton.set_size_request(50, 50)
        
        fixed = Gtk.Fixed()
        fixed.put(exitbutton, 0, 0)
        
        overlay.add_overlay(fixed)
        
"""
    def onOpen(self):
        print('Idle open')
        self.show_all()
        self.update = True
        print(111)
        threading.Thread(target=self.startPreview, args=()).start()

    def startPreview(self):
        while self.update:
            GLib.idle_add(self.showFrame)
            time.sleep(0.07)


    def showFrame(self):#демонстрация кадра на экран
        if(self.ret == False):
            self.cap.release()
            self.cap = cv2.VideoCapture(self.file)
            self.ret, self.frame = self.cap.read()
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])

        self.image_renderer.set_from_pixbuf(pb.copy())
        self.ret, self.frame = self.cap.read()

    def onClose(self):
        self.update = False
        self.cap.release()
        print('Idle close')

    def toScanner(self, widget): # функция перехода к QR коду
        self.update = False
        self.cap.release()
        self.parent.openBox(self, 1)

    # def close(self):
    #     print('close idle')





class ScannerBox(Gtk.Box):#форма сканирования qr кода
    def __init__(self, par):
        Gtk.Box.__init__(self)

        self.par = par

        self.camera = j.CameraCapture()

        self.qrdetect = j.QRDetect()
        self.qrcheck = j.QRCheck()
        self.frame = None
        self.scannerOn = True


        self.warning = False

        self.stack = Gtk.Overlay()
        self.add(self.stack)

        background = Gtk.Image.new_from_file('./video/photo1.png')
        self.stack.add(background)

        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('./video/photo1.png', 480, 800)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)

        ####LABEL
        labelfixed = Gtk.Fixed()
        self.stack.add_overlay(labelfixed)

        labelbox = Gtk.Box()
        labelbox.set_size_request(480, 100)
        #labelbox.set_margin_start(150)
        labelbox.override_background_color(0, Gdk.RGBA(0.1, 0.22, 0.06, 1))

        self.label = Gtk.Label(label="Код неверен")
        #self.label.set_markup("<span color='red' size='x-large'> Invalid code</span>")
        #self.label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        #self.label.set_valign(15)
        #self.label.set_valign()
        labelbox.add(self.label)
        labelfixed.put(labelbox, 0, 0)

        self.update = False
        ###LABEL END

    def onOpen(self):
        print('Scanner open')

        self.camera.start()

        self.show_all()
        self.setStatusText(0)

        self.update = True

        threading.Thread(target=self.startPreview, args=()).start()
        threading.Thread(target=self.qrCheck, args=()).start()

        #self.par.openBox(self, 0)

    def onClose(self):
        print('Scanner close')
        print(1)
        self.camera.stop()
        print(2)
        self.setStatusText(0)
        print(3)
        self.update = False
        print(4)

    def toIdle(self, widget):
        self.hide()
        self.update = False
        self.par.openBox(self, 0)
        print("toIdle")


    def toInstruction(self, widget):
        print(10)
        self.hide()
        self.update = False
        self.par.openBox(self, 2)
        print(11)
        print('toInstruction')

    def setStatusText(self, num):
        if num == 0: #0 = idle, 1 = invalid, 2 = used
            self.label.set_markup("<span font='Montserrat' foreground='#ebe6c0' weight='heavy' size='xx-large' letter-spacing ='2300'>     ПОДНЕСИТЕ QR-КОД</span>")
        elif num == 1:
            self.label.set_markup("<span font='Montserrat' foreground='#ebe6c0' weight='heavy' size='xx-large' letter-spacing ='2300'>    QR-КОД НЕ ПОДХОДИТ</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 2:
            self.label.set_markup("<span font='Montserrat' foreground='#ebe6c0' weight='heavy' size='large' letter-spacing ='2300'>  QR-КОД УЖЕ БЫЛ ИСПОЛЬЗОВАН</span>")
            threading.Thread(target=self.warningDissapear, args=()).start()
        elif num == 3:
            self.label.set_markup("<span font='Montserrat' foreground='#ebe6c0' weight='heavy' size='xx-large' letter-spacing ='2300'>        QR-КОД ПРИНЯТ</span>")
        elif num == 4:
            self.label.set_markup("<span color='#ffffff' size='x-large'>     Admin privet</span>")
        elif num == 5:
            self.label.set_markup("<span color='#ffffff' size='x-large'>     Destroy</span>")
            time.sleep(4)
        elif num == 6:
            self.label.set_markup("<span color='#ffffff' size='x-large'>     Настройки изменены</span>")
            time.sleep(3)
        elif num > 6:
            self.label.set_markup("<span color='#ffffff' size='x-large'>     Проливка "+str(num)+" секунд</span>")
            time.sleep(3)



    def warningDissapear(self):
        self.warning = True
        print('startWarning')
        time.sleep(4)
        print('endWarning')
        self.warning = False
        self.setStatusText(0)

    def startPreview(self):
        while self.update:
            GLib.idle_add(self.showFrame)
            time.sleep(0.1)

    def qrCheck(self):#функция проверки qr кода и выдачи результата

        time.sleep(1)

        start_time = time.time()

        while self.update:
            if self.frame is not None:

                print('CHECK QR')

                qrdata = self.qrdetect.detect(self.frame)

                if time.time()-start_time > 30:
                    self.update = False
                    time.sleep(0.5)
                    self.toIdle(None)

                if qrdata is not None:
                    qrresult = self.qrcheck.check(qrdata)
                    if qrresult == -1:
                        print("Invalid code")
                        if not self.warning:
                            self.setStatusText(1)
                            #4 sec wait

                    elif qrresult == -2:
                        print("Code already used")
                        if not self.warning:
                            self.setStatusText(2)
                            #4 sec wait
                    elif qrresult == -3:
                        print("Admin privet")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(4)
                    elif qrresult == -4:
                        global m
                        print("Destroy")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(5)
                        self.update = False
                        self.par.close()
                    elif qrresult == -5:
                        print("Settings")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(6)
                        time.sleep(10)
                        if not self.warning:
                            self.setStatusText(0)
                        start_time = time.time()



                    elif qrresult < -6:
                        print("Proliv")
                        time.sleep(1)
                        if not self.warning:
                            self.setStatusText(-qrresult)

                        servo = j.ServoAct()
                        servo.setActPosition()
                        time.sleep(0.4)
                        time.sleep(-qrresult)
                        servo.setIdlePosition()
                        time.sleep(0.4)
                        servo.hold()
                        time.sleep(2)
                        start_time = time.time()
                        if not self.warning:
                            self.setStatusText(0)


                    elif qrresult == 1:
                        print("Code is valid")
                        self.setStatusText(3)
                        self.qrcheck.applyLast()
                        self.update = False

                        time.sleep(0.5)
                        self.toInstruction(None)
                        #Servo go

            time.sleep(0.5)

        self.qrcheck.close()


    def showFrame(self):#демонстрация кадра на экран

        #print('tick')
        try:
            frame = self.camera.getFrame()
        except Exception:
            frame = self.frame
        frame = frame[0:220, 0:360]
        #frame = cv2.resize(frame, (800, 480))
        self.frame = frame.copy()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame,1)

        #overlay = cv2.imread('border.png')
        #frame = cv2.addWeighted(frame,0.8,overlay,0.1,0)

        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])

        pb = pb.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        pb = pb.scale_simple(480, 800, GdkPixbuf.InterpType.NEAREST)#GdkPixbuf.InterpType.NEAREST
        self.image_renderer.set_from_pixbuf(pb.copy())

        #try:
            #while not self.stopEvent.is_set():



        #except RuntimeError:
            #print("[INFO] caught a RuntimeError")


    # def close(self):
    #     print('close scanner')
    #     self.update = False


class AppWindow(Gtk.Window):#главная форма
    def __init__(self):


        Gtk.Window.__init__(self, title="Hello World")
        self.set_size_request(480, 800)
        self.modify_bg(Gtk.StateFlags.NORMAL,Gdk.color_parse("#000000"))

        self.idle = IdleBox(self)
        self.scanner = ScannerBox(self)
        self.instruct = InstructionBox(self)

        self.box = Gtk.Stack()

        self.add(self.box)

        self.box.add(self.idle)


        """
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)
        self.background = Gtk.Image.new_from_file('disp1.png')
       
        self.button = Gtk.Button(label='Test')
        self.button.set_property("opacity", 0.1)
        self.button.connect("clicked", self.on_button_clicked)
        self.overlay.add(self.background)
        self.overlay.add_overlay(self.button)
        """

    #def close(self):
    #    self.instruct.close()

    def destroySafe(self):
        Gtk.main_quit()
        self.idle.close()
        self.scanner.close()
        self.instruct.close()

    def destroy(self):
        GLib.idle_add(self.destroySafe)


    def openBoxSafe(self, widget, num):
        #0 - idle, 1 - scanner, 2 - instruct
        if widget is not None:
            self.box.remove(widget)
            widget.onClose()
        target = None

        if num == 0:
            target = self.idle
            print('0')
        elif num == 1:
            target = self.scanner
            print('1')
        elif num == 2:
            target = self.instruct
            print('2')

        self.box.add(target)
        target.onOpen()

        #self.box.remove(target)
        #self.show_all()

    def openBox(self, widget, num):
        GLib.idle_add(self.openBoxSafe, widget, num)

    def on_button_clicked(self, widget):
        print("Hello World")
        #win = ScannerWindow()
        #win.show_all()
        self.button.destroy()
        #

class main:
    def __init__(self): #консруктор
        self.win = AppWindow()
        self.win.connect("destroy", self.close)
        self.win.fullscreen()
        self.win.openBox(None, 0)
        self.win.show_all()
        Gtk.main()

    def close(self, widget):
         Gtk.main_quit()
         self.win.close()
         # self.win.scanner.close()
         # self.win.instruct.close()


m = main()

