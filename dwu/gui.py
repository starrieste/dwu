from pydoc import text
import threading

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from .wallpaper_manager import WallpaperManager

class GUI(App):
    def __init__(self):
        super().__init__()
        self.wallman = WallpaperManager()

    def build(self):
        layout = BoxLayout(orientation='vertical')  # buttons stacked vertically

        btn1 = Button(text='Update Wallpaper')
        btn2 = Button(text='Start check loop')
        btn3 = Button(text='Stop check loop')

        # the bind method passes the button as the first argument, which breaks my functions
        btn1.bind(on_press=lambda x: threading.Thread(target=self.wallman.update_wallpaper, daemon=True).start())
        btn2.bind(on_press=lambda x: threading.Thread(target=self.wallman.start_check_loop, daemon=True).start())
        btn3.bind(on_press=lambda x: threading.Thread(target=self.wallman.stop_check_loop, daemon=True).start())

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        return layout

def run_gui():
    GUI().run()
