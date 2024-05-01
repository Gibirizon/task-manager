# KIVY_DPI=395 KIVY_METRICS_DENSITY=1.5 python main.py --size 2400x1080
from kivy.config import Config

Config.set("graphics", "width", "540")
Config.set("graphics", "height", "1000")

from database.database import Database
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp


class MainScreenManager(ScreenManager):
    touch_down_x = 0
    previous_screen = []
    screen_names_to_titles = {
        "menu": "Menu",
        "tasks": "Daily Tasks",
        "goals": "Daily Goals",
        "timer": "Timer",
        "weekly_tasks": "Weekly Tasks",
        "notes": "Notes",
        "stats": "Statistics",
        "calendar": "Calendar",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # after click on nav button changing screen
    def change_screen(self, screen_name, save_previous=True):
        # test is next screen on left or right on navigation bar compared to current screen
        current_screen_index = self.screen_names.index(self.current_screen.name)
        next_screen_index = self.screen_names.index(screen_name)
        if next_screen_index < current_screen_index:
            self.transition.direction = "right"
        else:
            self.transition.direction = "left"

        # save previous (current) screen to be able to go back to it
        if self.current_screen.name != screen_name and save_previous:
            self.previous_screen.append(self.current_screen.name)
        # change current screen with proper direction
        self.current = screen_name

    # creating swiping animation to also change screen
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.touch_down_x = touch.x
            self.touch_down_y = touch.y
        return super().on_touch_down(touch)

    # swiping animation - switching screens
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # that's the correct touch
            touch.ungrab(self)
            swipe_width = self.touch_down_x - touch.x
            swipe_height = abs(self.touch_down_y - touch.y)
            if swipe_width > 0.1 * self.width and abs(swipe_width) > swipe_height:
                next_screen_index = (
                    self.screen_names.index(self.current_screen.name) + 1
                )
                if next_screen_index >= len(self.screen_names):
                    next_screen_index = 0
                self.transition.direction = "left"
            elif -swipe_width > 0.1 * self.width and abs(swipe_width) > swipe_height:
                next_screen_index = (
                    self.screen_names.index(self.current_screen.name) - 1
                )
                self.transition.direction = "right"
            else:
                return super().on_touch_up(touch)

            # add current screen to previous screen list
            self.previous_screen.append(self.current_screen.name)

            # change to new screen
            self.current = self.screen_names[next_screen_index]

            # adjust top bar title to the current displayed screen
            self.parent.ids.nav.adjust_top_bar_title(
                self.screen_names_to_titles[self.screen_names[next_screen_index]]
            )

        return super().on_touch_up(touch)

    def go_back_to_previous_screen(self, *args):
        print(self.previous_screen)
        if self.previous_screen:
            self.change_screen(self.previous_screen[-1], False)
            self.parent.ids.nav.adjust_top_bar_title(
                self.screen_names_to_titles[self.previous_screen.pop()]
            )


class MainScreen(Screen):
    db = Database()

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
        Builder.load_file("./modules/menu/menu.kv")
        Builder.load_file("./modules/top_bar/top_bar.kv")
        Builder.load_file("./modules/goals/goals.kv")
        Builder.load_file("./modules/calendar/calendar.kv")
        Builder.load_file("./modules/notes/notes.kv")
        Builder.load_file("./modules/stats/stats.kv")
        Builder.load_file("./modules/timer/timer.kv")
        Builder.load_file("./modules/weekly_tasks/weekly_tasks.kv")
        Builder.load_file("./modules/tasks/tasks.kv")
        return MainScreen()

    def on_stop(self):
        # close connection to db
        self.root.db.close_connection()
        return super().on_stop()


if __name__ == "__main__":
    TaskManager().run()
