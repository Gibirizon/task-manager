from datetime import date, datetime

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsItem, MDTabsItemIcon, MDTabsItemText

# Get the currently running instance of the app
app = MDApp.get_running_app()


class Stats(MDScreen):
    # Properties to hold the total and consecutive days information
    total_days = StringProperty("0 d")
    consecutive_days = StringProperty("0 d")
    category = StringProperty("tasks")
    date = 0

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        self.calculate_statistics(self.category)
        return super().on_pre_enter(*args)

    # Function to display two categories
    def create_categories(self):
        categories_info = [
            ["checkbox-marked-circle-auto-outline", "tasks", "Daily Tasks"],
            ["timeline-plus", "goals", "Daily Goals"],
        ]

        for category in categories_info:
            self.ids.categories.add_widget(
                MDTabsItem(
                    MDTabsItemIcon(
                        icon=category[0],
                    ),
                    MDTabsItemText(
                        text=category[2],
                    ),
                    on_release=lambda _, table_name=category[
                        1
                    ]: self.calculate_statistics(table_name),
                )
            )

    # Function to calculate and update statistics based on selected category
    def calculate_statistics(self, table_name):
        # set category - the same name as tables
        self.category = table_name
        self.date = self.get_date_in_seconds()

        # update database for present day
        self.update_database()

        self.calculate_total_completed_days()

        self.calculate_consecutive_days()

    def calculate_consecutive_days(self):
        self.consecutive_days = (
            f"{app.root.db.calculate_consecutive_days(self.category, self.date)} d"
        )

    def calculate_total_completed_days(self):
        self.total_days = f"{app.root.db.get_number_of_completed_days(self.category)} d"

    def update_database(self):
        all_items_completed = self.check_are_all_items_completed()

        today_item = app.root.db.get_today_element(self.date, self.category)
        if today_item:
            app.root.db.update_element(
                today_item[0], self.category, all_items_completed
            )
        else:
            app.root.db.create_element(self.date, self.category, all_items_completed)

    def get_date_in_seconds(self):
        current_date = date.today()
        # return seconds from 1970
        return datetime.fromisoformat(current_date.isoformat()).timestamp()

    def check_are_all_items_completed(self):
        # Retrieve all items from the selected table (e.g., tasks, goals)
        all_items = app.root.db.get_all_items(self.category)

        # Check if all planned tasks in the selected category are completed
        return all([x[-1] for x in all_items])
