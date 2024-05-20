from kivy.config import Config

# Set the dimensions of the application window
Config.set("graphics", "width", "540")
Config.set("graphics", "height", "1000")

from database.database import Database
from kivy.core.text import LabelBase
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp


# Custom ScreenManager to handle screen transitions and navigation logic
class MainScreenManager(ScreenManager):
    touch_down_x = 0  # x-coordinate of the touch down event
    previous_screen = []  # stack to keep track of previous screens for back navigation
    screen_names_to_titles = {  # mapping screen names to titles for the top bar
        "menu": "Menu",
        "tasks": "Daily Tasks",
        "goals": "Daily Goals",
        "timer": "Timer",
        "weekly_tasks": "Weekly Tasks",
        "stats": "Statistics",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Change screen based on navigation button click
    def change_screen(self, screen_name, save_previous=True):
        # Determine the transition direction based on the order of screens
        current_screen_index = self.screen_names.index(self.current_screen.name)
        next_screen_index = self.screen_names.index(screen_name)
        if next_screen_index < current_screen_index:
            self.transition.direction = "right"
        else:
            self.transition.direction = "left"

        # Save the current screen to the previous screens stack if needed
        if self.current_screen.name != screen_name and save_previous:
            self.previous_screen.append(self.current_screen.name)

        # Change the current screen
        self.current = screen_name

    # Handle touch down event to initiate screen swipe
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self.touch_down_x = touch.x
            self.touch_down_y = touch.y
        return super().on_touch_down(touch)

    # Handle touch up event to complete the swipe and change screen
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            swipe_width = self.touch_down_x - touch.x
            swipe_height = abs(self.touch_down_y - touch.y)

            # Swipe left to go to the next screen
            if swipe_width > 0.1 * self.width and abs(swipe_width) > swipe_height:
                next_screen_index = (
                    self.screen_names.index(self.current_screen.name) + 1
                )
                if next_screen_index >= len(self.screen_names):
                    next_screen_index = 0
                self.transition.direction = "left"
            # Swipe right to go to the previous screen
            elif -swipe_width > 0.1 * self.width and abs(swipe_width) > swipe_height:
                next_screen_index = (
                    self.screen_names.index(self.current_screen.name) - 1
                )
                self.transition.direction = "right"
            else:
                return super().on_touch_up(touch)

            # Add the current screen to the previous screens stack
            self.previous_screen.append(self.current_screen.name)

            # Change to the new screen
            self.current = self.screen_names[next_screen_index]

            # Adjust the top bar title to the current screen
            self.parent.ids.nav.adjust_top_bar_title(
                self.screen_names_to_titles[self.screen_names[next_screen_index]]
            )

        return super().on_touch_up(touch)

    # Navigate back to the previous screen
    def go_back_to_previous_screen(self, *args):
        if self.previous_screen:
            target_screen = self.previous_screen.pop()
            self.change_screen(target_screen, False)
            self.parent.ids.nav.adjust_top_bar_title(
                self.screen_names_to_titles[target_screen]
            )


# Main screen class which initializes the database
class MainScreen(Screen):
    db = Database()  # Initialize the database connection

    def __init__(self, **kw):
        super().__init__(**kw)

    # Handle navigation button click to change the screen
    def nav_button_click(self, screen_name):
        # Change the current screen by calling method on screen manager
        self.ids.sm.change_screen(screen_name)

        # Adjust top bar title to the current displayed screen
        self.ids.nav.adjust_top_bar_title(
            self.ids.sm.screen_names_to_titles[screen_name]
        )


# Main application class
class TaskManager(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  # Set the theme to dark mode

        # Load the kv files for different modules
        Builder.load_file("modules/to_do_list_base_classes/base.kv")
        Builder.load_file("./modules/menu/menu.kv")
        Builder.load_file("./modules/top_bar/top_bar.kv")
        Builder.load_file("./modules/goals/goals.kv")
        Builder.load_file("./modules/stats/stats.kv")
        Builder.load_file("./modules/timer/timer.kv")
        Builder.load_file("./modules/weekly_tasks/weekly_tasks.kv")
        Builder.load_file("./modules/tasks/tasks.kv")

        # Register custom font style
        LabelBase.register(
            name="lora",
            fn_regular="fonts/Lora-BoldItalic.ttf",
        )

        # Define custom font styles
        self.theme_cls.font_styles["lora"] = {
            "large": {
                "line-height": 1.64,
                "font-name": "lora",
                "font-size": dp(60),
            },
            "medium": {
                "line-height": 1.52,
                "font-name": "lora",
                "font-size": dp(46),
            },
            "small": {
                "line-height": 1.44,
                "font-name": "lora",
                "font-size": dp(24),
            },
        }
        return MainScreen()

    def on_start(self):
        # Initialize the navigation bar and create tabs
        self.root.ids.nav.ids.navigation_bar.create_tabs()

        # Calculate initial statistics for the "stats" screen
        self.root.ids.sm.get_screen("stats").calculate_statistics(
            "Daily tasks", "tasks"
        )
        return super().on_start()

    def on_stop(self):
        # Close the database connection when the app stops
        self.root.db.close_connection()
        return super().on_stop()


# Entry point of the application
if __name__ == "__main__":
    TaskManager().run()
