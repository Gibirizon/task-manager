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
        menu_items = [
            {
                "text": "Daily Tasks",
                "leading_icon": "checkbox-marked-circle-auto-outline",
                "leading_icon_color": "orange",
            },
            {
                "text": "Goals",
                "leading_icon": "timeline-plus",
                "leading_icon_color": "orange",
            },
            {
                "text": "Weekly Tasks",
                "leading_icon": "calendar-week",
                "leading_icon_color": "orange",
            },
        ]
        self.tabs_menu = MDDropdownMenu(caller=self.ids.btn, items=menu_items).open()

    # def on_pre_enter(self, *args):
    #     self.count_statistics("tasks")
    #     return super().on_pre_enter(*args)

    # def count_statistics(self, table_name):
    #     # get all items of the table which was chosen from dropdown list (by default daily tasks)
    #     all_elements = app.root.db.get_all_items(table_name)

    #     # check if all of the planned tasks are completed
    #     completed = all([x[-1] for x in all_elements])

    #     # add information to a database
    #     app.root.db.create_or_change_item_realisation(table_name, int(completed))
