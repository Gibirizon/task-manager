from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

app = MDApp.get_running_app()


class Stats(Screen):
    total_days = StringProperty("0 d")
    consecutive_days = StringProperty("0 d")

    def __init__(self, **kw):
        super().__init__(**kw)

    def tabs_menu_open(self):
        menu_elements_info = [
            ["checkbox-marked-circle-auto-outline", "tasks", "Daily Tasks"],
            ["timeline-plus", "goals", "Daily Goals"],
            ["calendar-week", "weekly_tasks", "Weekly Tasks"],
        ]
        menu_items = [
            {
                "text": element[2],
                "leading_icon": element[0],
                "leading_icon_color": "orange",
                "on_release": lambda text=element[2], table_name=element[
                    1
                ]: self.calculate_statistics(text, table_name),
            }
            for element in menu_elements_info
        ]
        self.tabs_menu = MDDropdownMenu(caller=self.ids.btn, items=menu_items).open()

    def on_pre_enter(self, *args):
        self.calculate_statistics("Daily tasks", "tasks")
        return super().on_pre_enter(*args)

    def calculate_statistics(self, text, table_name):
        # change button text
        self.ids.btn_text.text = text

        # get all items of the table which was chosen from dropdown list (by default daily tasks)
        all_elements = app.root.db.get_all_items(table_name)

        # check if all of the planned tasks are completed
        completed = all([x[-1] for x in all_elements])

        # add information to a database
        app.root.db.create_or_change_item_realisation(table_name, int(completed))
