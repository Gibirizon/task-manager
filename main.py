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
    touch_down_x = 0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # after click on nav button changing screen
    def change_screen(self, screen_name):
            # test is next screen on left or right on navigation bar compared to current screen
            current_screen_index = self.screen_names.index(self.current_screen.name)
            next_screen_index = self.screen_names.index(screen_name)
            if next_screen_index < current_screen_index:
                self.transition.direction = "right"
            else:
                self.transition.direction = "left"
            # change current screen with proper direction
            self.current = screen_name

    def on_touch_down(self, touch):
        self.touch_down_x = touch.x
        print(self.touch_down_x)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.touch_down_x - touch.x > 0.05 * self.width:
           next_screen_index = self.screen_names.index(self.current_screen.name) + 1
           if next_screen_index >= len(self.screen_names):
               next_screen_index = 0
           self.transition.direction = "left"
        elif touch.x - self.touch_down_x > 0.05 * self.width:
           next_screen_index = self.screen_names.index(self.current_screen.name) - 1
           self.transition.direction = "right"
        else:
            return super().on_touch_up(touch)
        self.current = self.screen_names[next_screen_index]
        return super().on_touch_up(touch)



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
