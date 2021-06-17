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

class IdleBox(Gtk.Box):#форма сканирования qr кода
    def __init__(self, parent):
        Gtk.Box.__init__(self)


        self.cap = cv2.VideoCapture("./video/v4.mp4")
        ret, self.frame = self.cap.read()
        self.stack = Gtk.Overlay()
        self.add(self.stack)
        background = Gtk.Image.new_from_file('disp2.png')
        self.stack.add(background)
        self.image = GdkPixbuf.Pixbuf.new_from_file_at_size('disp1.png', 480, 800)
        self.image_renderer = Gtk.Image.new_from_pixbuf(self.image)
        self.stack.add_overlay(self.image_renderer)
        button = Gtk.Button(label='Нажмите, чтобы начать')
        button.set_property("opacity", 0)
        button.connect("clicked", self.onClose)  # привязка тригера на переход к qr коду

        self.stack.add_overlay(button)

        ####LABEL


        #self.label.set_markup("<span color='red' size='x-large'> Invalid code</span>")
        #self.label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        #self.label.set_valign(15)
        #self.label.set_valign()


        self.update = False
        ###LABEL END

    def onOpen(self):
        print('Scanner open')
        self.show_all()

        self.update = True
        print(111)
        threading.Thread(target=self.startPreview, args=()).start()

        #self.par.openBox(self, 0)

    def onClose(self,widget):
        print('Scanner close')
        print(1)
        print(2)
        print(3)
        self.update = False
        print(4)





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
            time.sleep(0.07)

    def showFrame(self):#демонстрация кадра на экран

        #print('tick')

        ret, self.frame = self.cap.read()
        if(ret == False):
            self.cap.release()
            self.cap = cv2.VideoCapture("./video/v4.mp4")
            ret, self.frame = self.cap.read()
        #frame = self.camera.getFrame()
        #frame = frame[0:216, 0:360]
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        #overlay = cv2.imread('border.png')
        #frame = cv2.addWeighted(frame,0.8,overlay,0.1,0)

        pb = GdkPixbuf.Pixbuf.new_from_data(frame.tostring(),
                                            GdkPixbuf.Colorspace.RGB,
                                            False,
                                            8,
                                            frame.shape[1],
                                            frame.shape[0],
                                            frame.shape[2]*frame.shape[1])

        #pb = pb.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)
        #pb = pb.scale_simple(480, 800, GdkPixbuf.InterpType.NEAREST)#GdkPixbuf.InterpType.NEAREST
        self.image_renderer.set_from_pixbuf(pb.copy())

        #try:
            #while not self.stopEvent.is_set():



        #except RuntimeError:
            #print("[INFO] caught a RuntimeError")


    # def close(self):
    #     print('close scanner')
    #     self.update = False

class OneMorePlayer(Gtk.Box):

    def __init__(self):
        Gtk.Box.__init__(self)

        self.secs = int(round(time.time() * 1000))

        self.cap = None

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_drawing_area_draw)
        self.drawing_area.set_size_request(480, 800)
        self.add(self.drawing_area)

        #self.image = Gtk.Image()
        #self.image = Gtk.Image.new_from_file('disp2.png')
        #self.image.set_size_request(480, 800)
        #self.add(self.image)

        self.mymutex = threading.Lock()
        self.dimg = GdkPixbuf.Pixbuf.new_from_file('disp1.png')

        thread = threading.Thread(target = self.VideoLoop)
        #thread.daemon = True
        thread.start()
        self.show_all()

    def on_drawing_area_draw(self,widget,cr):
        #print('')
        #self.mymutex.acquire()
        #print('draw')
        Gdk.cairo_set_source_pixbuf(cr, self.dimg.copy(), 0, 0)
        cr.paint()
        now = int(round(time.time() * 1000))
        print(str(now-self.secs))
        self.secs = now
        #self.mymutex.release()

    def VideoLoop(self):

        filename = 'video.mp4'

        self.cap = cv2.VideoCapture(filename)
        print(self.cap.isOpened())

        #GLib.timeout_add(3, self.drawing_area.queue_draw)


        while True:
            #GLib.idle_add(self.showFrame)
            self.showFrame()
            time.sleep(0.03)
        #img = np.random.randint(255, size=(300, 600, 3))
        #isWritten = cv2.imwrite('image-2.png', img)

    def show(self):
        self.image.set_from_pixbuf(self.dimg.copy())

    def showFrame(self):
        #while True:
        #print('showFrame')
        ret, img = self.cap.read()

        #print(save)
        if img is not None:
            #save = cv2.imwrite('/home/pi/image-3.png', img)
            #print(save)
            #self.mymutex.acquire()
            #boxAllocation = self.drawing_area.get_allocation()
            #print(boxAllocation.width)
            #img = cv2.resize(img, (boxAllocation.width,\
            #                       boxAllocation.height))

            #img = cv2.resize(img, (480, 800))

            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # opencv by default load BGR colorspace. Gtk supports RGB hance the conversion
            self.dimg = GdkPixbuf.Pixbuf.new_from_data(img.tostring(),
                                                  GdkPixbuf.Colorspace.RGB,False,8,
                                                  img.shape[1],
                                                  img.shape[0],                                                      img.shape[2]*img.shape[1],None,None)

            #time.sleep(0.03)

            Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, self.drawing_area.queue_draw)
            #GLib.idle_add(self.drawing_area.queue_draw)


            #self.drawing_area.queue_draw()
            #self.drawing_area.draw()
            #self.mymutex.release()

            #time.sleep(0.1)
            if ((cv2.waitKey(30) & 0xFF) == ord('q')):
                print('off')
        else:
            #self.mymutex.release()
            print('end of file')




class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_size_request(480, 800)

        self.idle = IdleBox(self)
        self.box = Gtk.Stack()

        self.add(self.box)

        self.box.add(self.idle)
    def start(self):
        self.idle.onOpen()


if __name__ == '__main__':
        window = ApplicationWindow()
        ##window.setup_objects_and_events()
        window.fullscreen()
        window.start()
        window.show_all()
        Gtk.main()
