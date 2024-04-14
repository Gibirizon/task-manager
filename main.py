# KIVY_DPI=395 KIVY_METRICS_DENSITY=1.5 python main.py --size 2400x1080
from kivy.config import Config

Config.set("graphics", "width", "540")
Config.set("graphics", "height", "1000")

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp

Builder.load_file("./modules/menu/menu.kv")
Builder.load_file("./modules/top_bar/top_bar.kv")
Builder.load_file("./modules/tasks/tasks.kv")
Builder.load_file("./modules/goals/goals.kv")
Builder.load_file("./modules/calendar/calendar.kv")
Builder.load_file("./modules/notes/notes.kv")
Builder.load_file("./modules/stats/stats.kv")
Builder.load_file("./modules/timer/timer.kv")
Builder.load_file("./modules/weekly_tasks/weekly_tasks.kv")


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # after click on nav button changing screen
    def change_screen(self, screen_name):
        self.current = screen_name


class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def nav_button_click(self, screen_name, screen_title):
        # changing the current screen by calling method on screen manager
        self.ids.sm.change_screen(screen_name)

        # adjust top bar title to the current displayed screen
        self.ids.nav.adjust_top_bar_title(screen_title)


class TaskManager(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"


if __name__ == "__main__":
    TaskManager().run()
