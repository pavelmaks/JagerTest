import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11

import vlc

MRL = "./video/1.mp4"  # File to play
WIDTH = 480
HEIGHT = 800


class IdleBox(Gtk.Box):  # стартовая форма

    def __init__(self, parent):
        Gtk.Box.__init__(self)

        self.parent = parent
        # self.videoPlayer = VideoPlayer()

        overlay = Gtk.Overlay()
        self.add(overlay)

        draw_area = Gtk.DrawingArea()
        ##self.draw_area.set_size_request(WIDTH, HEIGHT)

        draw_area.connect("realize", self._realized)

        self.add(draw_area)

        button = Gtk.Button(label='Нажмите, чтобы начать')
        button.set_property("opacity", 0)
        button.connect("clicked", self.onClose)  # привязка тригера на переход к qr коду

        overlay.add_overlay(button)

        """
        exitbutton = Gtk.Button(label='X')
        #exitbutton.set_property('opacity', 0)
        exitbutton.connect("clicked", parent.destroy)
        exitbutton.set_size_request(50, 50)

        fixed = Gtk.Fixed()
        fixed.put(exitbutton, 0, 0)

        overlay.add_overlay(fixed)

"""
    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib", "--input-repeat=-1")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        print(win_id)
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()


    def onOpen(self):
        print('Idle open')
        self.show_all()

    def onClose(self):
        print('Idle close')


    # def close(self):
    #     print('close idle')


class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.set_size_request(480, 800)

        self.idle = IdleBox(self)
        self.box = Gtk.Stack()

        self.add(self.box)

        self.box.add(self.idle)



        '''
        Gtk.Window.__init__(self, title="Python-Vlc Media Player")
        self.is_player_active = False
        self.connect("destroy", Gtk.main_quit)

        self.button = Gtk.Button(label='Нажмите, чтобы начать')
        self.button.set_property("opacity", 0)
        self.button.connect("clicked", self.stop_player)
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(WIDTH, HEIGHT)

        self.draw_area.connect("realize", self._realized)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.add(self.button)
        self.vbox.pack_start(self.draw_area, True, True, 0)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):
        self.button = Gtk.Button(label='Нажмите, чтобы начать')
        self.button.set_property("opacity", 0)
        self.button.connect("clicked", self.stop_player)
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(WIDTH, HEIGHT)

        self.draw_area.connect("realize", self._realized)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.add(self.button)
        self.vbox.pack_start(self.draw_area, True, True, 0)
    

    def stop_player(self, widget, data=None):
        self.player.stop()
        self.is_player_active = False


    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--no-xlib", "--input-repeat=-1")
        self.player = self.vlcInstance.media_player_new()
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.player.play()
        self.playback_button.set_image(self.pause_image)
        self.is_player_active = True
    '''

if __name__ == '__main__':
        window = ApplicationWindow()
        ##window.setup_objects_and_events()
        window.fullscreen()
        window.show_all()
        Gtk.main()
        print(1)
        window.player.stop()
        print(2)
        window.vlcInstance.release()
        print(3)