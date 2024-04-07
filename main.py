# KIVY_DPI=395 KIVY_METRICS_DENSITY=3.15 python main.py --size 2400x1080
from kivy.config import Config

Config.set("graphics", "width", "540")
Config.set("graphics", "height", "1000")

from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp


class StartScreen(RelativeLayout):
    pass


class TaskManager(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"


if __name__ == "__main__":
    TaskManager().run()
